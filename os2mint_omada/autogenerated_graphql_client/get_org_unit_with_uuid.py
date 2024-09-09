# Generated by ariadne-codegen on 2024-09-09 14:34
# Source: queries.graphql

from typing import List
from uuid import UUID

from .base_model import BaseModel


class GetOrgUnitWithUuid(BaseModel):
    org_units: "GetOrgUnitWithUuidOrgUnits"


class GetOrgUnitWithUuidOrgUnits(BaseModel):
    objects: List["GetOrgUnitWithUuidOrgUnitsObjects"]


class GetOrgUnitWithUuidOrgUnitsObjects(BaseModel):
    uuid: UUID


GetOrgUnitWithUuid.update_forward_refs()
GetOrgUnitWithUuidOrgUnits.update_forward_refs()
GetOrgUnitWithUuidOrgUnitsObjects.update_forward_refs()
