# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from __future__ import annotations

from itertools import chain
from typing import NewType
from uuid import UUID

import structlog
from more_itertools import one
from more_itertools import only
from ramodels.mo import Employee
from ramodels.mo import Validity as RAValidity
from ramodels.mo._shared import UUIDBase
from ramodels.mo.details import Engagement

from os2mint_omada.autogenerated_graphql_client import GraphQLClient
from os2mint_omada.sync.models import Address
from os2mint_omada.sync.models import ITUser
from os2mint_omada.sync.models import Validity
from os2mint_omada.util import validity_union

logger = structlog.stdlib.get_logger()

ITSystems = NewType("ITSystems", dict[str, UUID])


class MO:
    def __init__(self, graphql_client: GraphQLClient) -> None:
        self.graphql_client = graphql_client

    async def get_it_systems(self, user_keys: list[str]) -> ITSystems:
        result = await self.graphql_client.get_it_systems(user_keys=user_keys)
        return ITSystems(
            {o.current.user_key: o.current.uuid for o in result.objects if o.current}
        )

    async def get_classes(self, facet_user_key: str) -> dict[str, UUID]:
        result = await self.graphql_client.get_classes(user_keys=[facet_user_key])
        facet = one(result.objects).current
        assert facet is not None
        return {c.user_key: c.uuid for c in facet.classes}

    async def get_employee_uuid_from_user_key(self, user_key: str) -> UUID | None:
        result = await self.graphql_client.get_employee_uuid_from_user_key(
            user_keys=[user_key]
        )
        engagements = result.objects
        if not engagements:
            return None
        objects = chain.from_iterable(e.validities for e in engagements)
        employees = chain.from_iterable(o.person for o in objects)
        uuids = {e.uuid for e in employees}
        return one(uuids)  # it's an error if different UUIDs are returned

    async def get_employee_uuid_from_cpr(self, cpr: str) -> UUID | None:
        result = await self.graphql_client.get_employee_uuid_from_cpr(cpr_numbers=[cpr])
        employees = result.objects
        if not employees:
            return None
        uuids = {e.uuid for e in employees}
        return one(uuids)  # it's an error if different UUIDs are returned

    async def get_employee_states(self, uuid: UUID) -> set[Employee]:
        result = await self.graphql_client.get_employee_states(uuids=[uuid])
        employee = only(result.objects)
        if employee is None:
            return set()
        return {Employee.parse_obj(v) for v in employee.validities}

    async def get_current_employee_state(self, uuid: UUID) -> Employee | None:
        result = await self.graphql_client.get_current_employee_state(uuids=[uuid])
        employee = only(result.objects)
        if employee is None:
            return None
        return Employee.parse_obj(employee.current)

    async def get_employee_addresses(
        self, uuid: UUID, address_types: list[UUID] | None = None
    ) -> set[Address]:
        result = await self.graphql_client.get_employee_addresses(
            employee_uuids=[uuid],
            address_types=address_types,
        )
        employee = only(result.objects)
        if employee is None:
            return set()
        addresses = chain.from_iterable(v.addresses for v in employee.validities)
        return {
            Address(
                uuid=address.uuid,
                value=address.value,
                address_type=address.address_type.uuid,
                person=one({p.uuid for p in (address.person or [])}),
                visibility=(
                    visibility.uuid
                    if (visibility := address.visibility) is not None
                    else None
                ),
                engagement=only({e.uuid for e in (address.engagement or [])}),
                validity=Validity(
                    start=address.validity.from_,
                    end=to if (to := address.validity.to) is not None else None,
                ),
            )
            for address in addresses
        }

    async def get_employee_engagements(self, uuid: UUID) -> set[Engagement]:
        result = await self.graphql_client.get_employee_engagements(
            employee_uuids=[uuid]
        )
        employee = only(result.objects)
        if employee is None:
            return set()
        engagements = chain.from_iterable(v.engagements for v in employee.validities)
        return {
            Engagement.from_simplified_fields(
                uuid=engagement.uuid,
                user_key=engagement.user_key,
                org_unit_uuid=one({o.uuid for o in engagement.org_unit}),
                person_uuid=one({p.uuid for p in engagement.person}),
                job_function_uuid=engagement.job_function.uuid,
                engagement_type_uuid=engagement.engagement_type.uuid,
                primary_uuid=(
                    primary.uuid
                    if (primary := engagement.primary) is not None
                    else None
                ),
                from_date=engagement.validity.from_.isoformat(),
                to_date=(
                    to.isoformat()
                    if (to := engagement.validity.to) is not None
                    else None
                ),
            )
            for engagement in engagements
        }

    async def get_employee_it_users(
        self, uuid: UUID, it_systems: list[UUID]
    ) -> set[ITUser]:
        result = await self.graphql_client.get_employee_it_users(
            employee_uuids=[uuid],
            it_system_uuids=it_systems,
        )
        employee = only(result.objects)
        if employee is None:
            return set()
        it_users = chain.from_iterable(v.itusers for v in employee.validities)
        return {
            ITUser(
                uuid=it_user.uuid,
                user_key=it_user.user_key,
                it_system=it_user.itsystem.uuid,
                person=one({p.uuid for p in (it_user.person or [])}),
                engagement=only({e.uuid for e in (it_user.engagement or [])}),
                validity=Validity(
                    start=it_user.validity.from_,
                    end=to if (to := it_user.validity.to) is not None else None,
                ),
            )
            for it_user in it_users
        }

    async def get_org_unit_with_it_system_user_key(self, user_key: str) -> UUID:
        result = await self.graphql_client.get_org_unit_with_it_system_user_key(
            user_keys=[user_key]
        )
        it_users = result.objects
        if not it_users:
            raise KeyError(f"No organisation unit with {user_key=} found")
        validities = chain.from_iterable(u.validities for u in it_users)
        uuids = {ou.uuid for v in validities for ou in v.org_unit or []}
        return one(uuids)  # it's an error if different UUIDs are returned

    async def get_org_unit_with_uuid(self, uuid: UUID) -> UUID:
        result = await self.graphql_client.get_org_unit_with_uuid(uuids=[uuid])
        try:
            org_unit = one(result.objects)
        except ValueError as e:
            raise KeyError(f"No organisation unit with {uuid=} found") from e
        return org_unit.uuid

    async def get_org_unit_with_user_key(self, user_key: str) -> UUID:
        result = await self.graphql_client.get_org_unit_with_user_key(
            user_keys=[user_key],
        )
        try:
            org_unit = one(result.objects)
        except ValueError as e:
            raise KeyError(f"No organisation unit with {user_key=} found") from e
        return org_unit.uuid

    async def get_org_unit_validity(self, uuid: UUID) -> RAValidity:
        result = await self.graphql_client.get_org_unit_validity(
            uuids=[uuid],
        )
        org_unit = one(result.objects)
        # Consolidate validities from all past/present/future versions of the org unit
        validities = (
            RAValidity(
                from_date=validity.validity.from_date,
                to_date=validity.validity.to_date,
            )
            for validity in org_unit.validities
        )
        return validity_union(*validities)

    async def delete_address(self, obj: Address) -> None:
        logger.info("Deleting address", address=obj)
        assert obj.uuid is not None
        await self.graphql_client.delete_address(uuid=obj.uuid)

    async def delete_engagement(self, obj: UUIDBase) -> None:
        logger.info("Deleting engagement", engagement=obj)
        await self.graphql_client.delete_engagement(uuid=obj.uuid)

    async def delete_it_user(self, obj: ITUser) -> None:
        logger.info("Deleting it_user", it_user=obj)
        assert obj.uuid is not None
        await self.graphql_client.delete_it_user(uuid=obj.uuid)
