from typing import List
from typing import Optional
from uuid import UUID

from .base_model import BaseModel


class GetOrgUnit(BaseModel):
    org_units: "GetOrgUnitOrgUnits"


class GetOrgUnitOrgUnits(BaseModel):
    objects: List["GetOrgUnitOrgUnitsObjects"]


class GetOrgUnitOrgUnitsObjects(BaseModel):
    uuid: UUID
    validities: List["GetOrgUnitOrgUnitsObjectsValidities"]


class GetOrgUnitOrgUnitsObjectsValidities(BaseModel):
    user_key: str
    name: str
    parent_uuid: Optional[UUID]
    unit_type_response: Optional["GetOrgUnitOrgUnitsObjectsValiditiesUnitTypeResponse"]


class GetOrgUnitOrgUnitsObjectsValiditiesUnitTypeResponse(BaseModel):
    validities: List["GetOrgUnitOrgUnitsObjectsValiditiesUnitTypeResponseValidities"]


class GetOrgUnitOrgUnitsObjectsValiditiesUnitTypeResponseValidities(BaseModel):
    name: str


GetOrgUnit.update_forward_refs()
GetOrgUnitOrgUnits.update_forward_refs()
GetOrgUnitOrgUnitsObjects.update_forward_refs()
GetOrgUnitOrgUnitsObjectsValidities.update_forward_refs()
GetOrgUnitOrgUnitsObjectsValiditiesUnitTypeResponse.update_forward_refs()
GetOrgUnitOrgUnitsObjectsValiditiesUnitTypeResponseValidities.update_forward_refs()
