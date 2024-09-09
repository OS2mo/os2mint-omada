# Generated by ariadne-codegen on 2024-09-09 14:40
# Source: queries.graphql

from datetime import datetime
from typing import List
from typing import Optional
from uuid import UUID

from pydantic import Field

from .base_model import BaseModel


class GetEmployeeItUsers(BaseModel):
    employees: "GetEmployeeItUsersEmployees"


class GetEmployeeItUsersEmployees(BaseModel):
    objects: List["GetEmployeeItUsersEmployeesObjects"]


class GetEmployeeItUsersEmployeesObjects(BaseModel):
    validities: List["GetEmployeeItUsersEmployeesObjectsValidities"]


class GetEmployeeItUsersEmployeesObjectsValidities(BaseModel):
    itusers: List["GetEmployeeItUsersEmployeesObjectsValiditiesItusers"]


class GetEmployeeItUsersEmployeesObjectsValiditiesItusers(BaseModel):
    uuid: UUID
    external_id: Optional[str]
    user_key: str
    itsystem: "GetEmployeeItUsersEmployeesObjectsValiditiesItusersItsystem"
    person: Optional[List["GetEmployeeItUsersEmployeesObjectsValiditiesItusersPerson"]]
    engagement: Optional[
        List["GetEmployeeItUsersEmployeesObjectsValiditiesItusersEngagement"]
    ]
    validity: "GetEmployeeItUsersEmployeesObjectsValiditiesItusersValidity"


class GetEmployeeItUsersEmployeesObjectsValiditiesItusersItsystem(BaseModel):
    uuid: UUID


class GetEmployeeItUsersEmployeesObjectsValiditiesItusersPerson(BaseModel):
    uuid: UUID


class GetEmployeeItUsersEmployeesObjectsValiditiesItusersEngagement(BaseModel):
    uuid: UUID


class GetEmployeeItUsersEmployeesObjectsValiditiesItusersValidity(BaseModel):
    from_: datetime = Field(alias="from")
    to: Optional[datetime]


GetEmployeeItUsers.update_forward_refs()
GetEmployeeItUsersEmployees.update_forward_refs()
GetEmployeeItUsersEmployeesObjects.update_forward_refs()
GetEmployeeItUsersEmployeesObjectsValidities.update_forward_refs()
GetEmployeeItUsersEmployeesObjectsValiditiesItusers.update_forward_refs()
GetEmployeeItUsersEmployeesObjectsValiditiesItusersItsystem.update_forward_refs()
GetEmployeeItUsersEmployeesObjectsValiditiesItusersPerson.update_forward_refs()
GetEmployeeItUsersEmployeesObjectsValiditiesItusersEngagement.update_forward_refs()
GetEmployeeItUsersEmployeesObjectsValiditiesItusersValidity.update_forward_refs()
