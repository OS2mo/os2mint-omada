# Generated by ariadne-codegen on 2024-08-22 18:07
# Source: queries.graphql

from datetime import datetime
from typing import List
from typing import Optional
from uuid import UUID

from pydantic import Field

from .base_model import BaseModel


class GetEmployeeEngagements(BaseModel):
    employees: "GetEmployeeEngagementsEmployees"


class GetEmployeeEngagementsEmployees(BaseModel):
    objects: List["GetEmployeeEngagementsEmployeesObjects"]


class GetEmployeeEngagementsEmployeesObjects(BaseModel):
    validities: List["GetEmployeeEngagementsEmployeesObjectsValidities"]


class GetEmployeeEngagementsEmployeesObjectsValidities(BaseModel):
    engagements: List["GetEmployeeEngagementsEmployeesObjectsValiditiesEngagements"]


class GetEmployeeEngagementsEmployeesObjectsValiditiesEngagements(BaseModel):
    uuid: UUID
    user_key: str
    org_unit: List["GetEmployeeEngagementsEmployeesObjectsValiditiesEngagementsOrgUnit"]
    person: List["GetEmployeeEngagementsEmployeesObjectsValiditiesEngagementsPerson"]
    job_function: (
        "GetEmployeeEngagementsEmployeesObjectsValiditiesEngagementsJobFunction"
    )
    engagement_type: (
        "GetEmployeeEngagementsEmployeesObjectsValiditiesEngagementsEngagementType"
    )
    primary: Optional[
        "GetEmployeeEngagementsEmployeesObjectsValiditiesEngagementsPrimary"
    ]
    validity: "GetEmployeeEngagementsEmployeesObjectsValiditiesEngagementsValidity"


class GetEmployeeEngagementsEmployeesObjectsValiditiesEngagementsOrgUnit(BaseModel):
    uuid: UUID


class GetEmployeeEngagementsEmployeesObjectsValiditiesEngagementsPerson(BaseModel):
    uuid: UUID


class GetEmployeeEngagementsEmployeesObjectsValiditiesEngagementsJobFunction(BaseModel):
    uuid: UUID


class GetEmployeeEngagementsEmployeesObjectsValiditiesEngagementsEngagementType(
    BaseModel
):
    uuid: UUID


class GetEmployeeEngagementsEmployeesObjectsValiditiesEngagementsPrimary(BaseModel):
    uuid: UUID


class GetEmployeeEngagementsEmployeesObjectsValiditiesEngagementsValidity(BaseModel):
    from_: datetime = Field(alias="from")
    to: Optional[datetime]


GetEmployeeEngagements.update_forward_refs()
GetEmployeeEngagementsEmployees.update_forward_refs()
GetEmployeeEngagementsEmployeesObjects.update_forward_refs()
GetEmployeeEngagementsEmployeesObjectsValidities.update_forward_refs()
GetEmployeeEngagementsEmployeesObjectsValiditiesEngagements.update_forward_refs()
GetEmployeeEngagementsEmployeesObjectsValiditiesEngagementsOrgUnit.update_forward_refs()
GetEmployeeEngagementsEmployeesObjectsValiditiesEngagementsPerson.update_forward_refs()
GetEmployeeEngagementsEmployeesObjectsValiditiesEngagementsJobFunction.update_forward_refs()
GetEmployeeEngagementsEmployeesObjectsValiditiesEngagementsEngagementType.update_forward_refs()
GetEmployeeEngagementsEmployeesObjectsValiditiesEngagementsPrimary.update_forward_refs()
GetEmployeeEngagementsEmployeesObjectsValiditiesEngagementsValidity.update_forward_refs()