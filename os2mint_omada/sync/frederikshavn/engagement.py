# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from __future__ import annotations

import asyncio
from collections import defaultdict
from uuid import UUID

import structlog
from fastramqpi.ramqp.depends import handle_exclusively_decorator
from more_itertools import only
from pydantic import parse_obj_as

from os2mint_omada.mo import MO
from os2mint_omada.omada.api import OmadaAPI
from os2mint_omada.util import validity_intersection

from ...autogenerated_graphql_client import EngagementCreateInput
from ...autogenerated_graphql_client import RAValidityInput
from ..models import ComparableEngagement
from ..models import Engagement
from .models import FrederikshavnOmadaUser

logger = structlog.stdlib.get_logger()


@handle_exclusively_decorator(key=lambda employee_uuid, *_, **__: employee_uuid)
async def sync_engagements(
    employee_uuid: UUID,
    mo: MO,
    omada_api: OmadaAPI,
) -> None:
    logger.info("Synchronising engagements", employee_uuid=employee_uuid)

    # Get current user data from MO
    employee_states = await mo.get_employee_states(employee_uuid)
    assert employee_states
    cpr_number = only({e.cpr_number for e in employee_states})

    if cpr_number is None:
        logger.warning(
            "Cannot synchronise employee without CPR number",
            employee_uuid=employee_uuid,
        )
        return

    mo_engagements = await mo.get_employee_engagements(uuid=employee_uuid)

    # Get current user data from Omada
    # Frederikshavn stores CPR numbers in Omada using the 'xxxxxx-xxxx' format, whereas
    # MO stores it as 'xxxxxxxxxx'. We search both variations to be sure.
    assert len(cpr_number) == 10
    cpr_number_with_dash = f"{cpr_number[:6]}-{cpr_number[6:]}"
    raw_omada_users = await omada_api.get_users_by(
        "C_CPRNUMBER", [cpr_number, cpr_number_with_dash]
    )
    omada_users = parse_obj_as(list[FrederikshavnOmadaUser], raw_omada_users)

    # Get MO classes configuration
    job_functions = await mo.get_classes("engagement_job_function")

    # Primary class for engagements created for omada users
    primary_types = await mo.get_classes("primary_type")
    primary_type_uuid = primary_types["primary"]

    # Engagement type for engagements created for omada users
    engagement_types = await mo.get_classes("engagement_type")
    engagement_type_uuid = engagement_types["omada_manually_created"]

    # Only process engagements we know Omada is authoritative for (created by us)
    # to avoid deleting those that have nothing to do with Omada.
    mo_omada_engagements = [
        e for e in mo_engagements if e.engagement_type == engagement_type_uuid
    ]

    # Existing engagements in MO
    existing: defaultdict[ComparableEngagement, set[Engagement]] = defaultdict(set)
    for mo_engagement in mo_omada_engagements:
        comparable_engagement = ComparableEngagement(**mo_engagement.dict())
        existing[comparable_engagement].add(mo_engagement)

    # Desired engagements from Omada
    async def build_comparable_engagement(
        omada_user: FrederikshavnOmadaUser,
    ) -> ComparableEngagement:
        # Engagements for Omada users are linked to the org unit through the org unit's
        # user_key.
        org_unit_uuid = await mo.get_org_unit_with_user_key(omada_user.org_unit)

        # The org unit's validity is needed to ensure the engagement's validity
        # does not lie outside this interval.
        org_unit_validity = await mo.get_org_unit_validity(org_unit_uuid)
        try:
            job_function_uuid = job_functions[
                omada_user.job_title  # type: ignore[index]
            ]
        except KeyError:
            # Fallback job function for engagements if the job title from Omada does
            # not exist in MO.
            job_function_uuid = job_functions["not_applicable"]
        return ComparableEngagement(
            user_key="",
            person=employee_uuid,
            org_unit=org_unit_uuid,
            job_function=job_function_uuid,
            engagement_type=engagement_type_uuid,
            primary=primary_type_uuid,
            validity=validity_intersection(omada_user.validity, org_unit_validity),
        )

    desired_tuples = await asyncio.gather(
        *(build_comparable_engagement(omada_user) for omada_user in omada_users)
    )
    desired: set[ComparableEngagement] = set(desired_tuples)

    # Delete excess existing
    excess: set[Engagement] = set()
    for comparable_engagement, engagements in existing.items():
        first, *duplicate = engagements
        excess.update(duplicate)
        if comparable_engagement not in desired:
            excess.add(first)
    if excess:
        logger.info("Deleting excess engagements", engagements=excess)
        await asyncio.gather(*(mo.delete_engagement(a) for a in excess))

    # Create missing desired
    missing_comparable = desired - existing.keys()
    missing_mo = [Engagement(**engagement.dict()) for engagement in missing_comparable]
    if missing_mo:
        logger.info("Creating missing engagements", engagements=missing_mo)
        for missing in missing_mo:
            await mo.graphql_client.create_engagement(
                EngagementCreateInput(
                    user_key=missing.user_key,
                    person=missing.person,
                    org_unit=missing.org_unit,
                    job_function=missing.job_function,
                    engagement_type=missing.engagement_type,
                    primary=missing.primary,
                    validity=RAValidityInput(
                        from_=missing.validity.start,
                        to=missing.validity.end,
                    ),
                )
            )
