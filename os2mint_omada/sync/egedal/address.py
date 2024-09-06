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
from ramodels.mo import Validity
from ramodels.mo._shared import AddressType
from ramodels.mo._shared import PersonRef
from ramodels.mo._shared import Visibility
from ramodels.mo.details import Address

from os2mint_omada.mo import MO
from os2mint_omada.omada.api import OmadaAPI
from os2mint_omada.sync.models import RAComparableMixin
from os2mint_omada.sync.models import RAStripUserKeyMixin

from ...autogenerated_graphql_client import AddressCreateInput
from ...autogenerated_graphql_client import RAValidityInput
from .models import EgedalOmadaUser

logger = structlog.stdlib.get_logger()


class ComparableAddress(RAStripUserKeyMixin, RAComparableMixin, Address):
    pass


@handle_exclusively_decorator(key=lambda employee_uuid, *_, **__: employee_uuid)
async def sync_addresses(
    employee_uuid: UUID,
    mo: MO,
    omada_api: OmadaAPI,
) -> None:
    logger.info("Synchronising addresses", employee_uuid=employee_uuid)

    # Get current user data from MO
    employee_states = await mo.get_employee_states(employee_uuid)
    assert employee_states
    cpr_number = only({e.cpr_no for e in employee_states})

    if cpr_number is None:
        logger.warning(
            "Cannot synchronise employee without CPR number",
            employee_uuid=employee_uuid,
        )
        return

    # Maps from Omada user attribute to employee address type (class) user key in MO
    address_map: dict[str, str] = {
        "email": "OmadaEmailEmployee",
        "phone": "OmadaPhoneEmployee",
        "cellphone": "OmadaMobilePhoneEmployee",
    }

    # Get MO classes configuration
    address_types = await mo.get_classes("employee_address_type")
    omada_address_types = [address_types[user_key] for user_key in address_map.values()]

    # Visibility class for created addresses
    visibility_classes = await mo.get_classes("visibility")
    visibility_uuid = visibility_classes["Public"]

    # Get current user data from MO
    mo_addresses = await mo.get_employee_addresses(
        uuid=employee_uuid,
        address_types=omada_address_types,
    )

    # Get current user data from Omada. Note that we are fetching ALL Omada users for
    # the CPR-number to avoid deleting too many addresses
    raw_omada_users = await omada_api.get_users_by("C_EMPLOYEEID", [cpr_number])
    omada_users = parse_obj_as(list[EgedalOmadaUser], raw_omada_users)

    # Existing addresses in MO
    existing: defaultdict[ComparableAddress, set[Address]] = defaultdict(set)
    for mo_address in mo_addresses:
        comparable_address = ComparableAddress(**mo_address.dict())
        existing[comparable_address].add(mo_address)

    # Desired addresses from Omada
    desired = set()
    for omada_user in omada_users:
        for omada_attr, mo_address_user_key in address_map.items():
            omada_value = getattr(omada_user, omada_attr)
            if omada_value is None:
                continue
            c = ComparableAddress(  # type: ignore[call-arg]
                value=omada_value,
                address_type=AddressType(uuid=address_types[mo_address_user_key]),
                person=PersonRef(uuid=employee_uuid),
                visibility=Visibility(uuid=visibility_uuid),
                validity=Validity(
                    from_date=omada_user.validity.from_date,
                    to_date=omada_user.validity.to_date,
                ),
            )
            desired.add(c)

    # Delete excess existing
    excess: set[Address] = set()
    for comparable_address, addresses in existing.items():
        first, *duplicate = addresses
        excess.update(duplicate)
        if comparable_address not in desired:
            excess.add(first)
    if excess:
        logger.info("Deleting excess addresses", addresses=excess)
        await asyncio.gather(*(mo.delete_address(a) for a in excess))

    # Create missing desired
    missing_comparable = desired - existing.keys()
    missing_mo = [Address(**address.dict()) for address in missing_comparable]
    if missing_mo:
        logger.info("Creating missing addresses", addresses=missing_mo)
        for missing in missing_mo:
            assert missing.person is not None
            assert missing.visibility is not None
            await mo.graphql_client.create_address(
                AddressCreateInput(
                    value=missing.value,
                    address_type=missing.address_type.uuid,
                    person=missing.person.uuid,
                    visibility=missing.visibility.uuid,
                    validity=RAValidityInput(
                        from_=missing.validity.from_date,
                        to=missing.validity.to_date,
                    ),
                )
            )
