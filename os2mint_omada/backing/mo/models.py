# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from uuid import UUID

from more_itertools import one
from pydantic import BaseModel
from pydantic import root_validator
from ramodels.mo.details import Address as MOAddress
from ramodels.mo.details import Engagement as MOEngagement
from ramodels.mo.details import ITUser as MOITUser


class Address(MOAddress):
    @root_validator(pre=True)
    def convert_graphql(cls, values: dict) -> dict:
        values["person"] = one(values["person"])
        return values


class Engagement(MOEngagement):
    @root_validator(pre=True)
    def convert_graphql(cls, values: dict) -> dict:
        values["person"] = one(values["person"])
        values["org_unit"] = {"uuid": values.pop("org_unit_uuid")}
        return values


class ITUser(MOITUser):
    @root_validator(pre=True)
    def convert_graphql(cls, values: dict) -> dict:
        values["person"] = one(values["person"])
        values["itsystem"] = {"uuid": values.pop("itsystem_uuid")}
        return values


class MOEmployee(BaseModel):
    uuid: UUID
    engagements: list[Engagement]
    addresses: list[Address]
    itusers: list[ITUser]
