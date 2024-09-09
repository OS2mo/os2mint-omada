# Generated by ariadne-codegen on 2024-09-09 14:34
# Source: queries.graphql

from uuid import UUID

from .base_model import BaseModel


class CreateEmployee(BaseModel):
    employee_create: "CreateEmployeeEmployeeCreate"


class CreateEmployeeEmployeeCreate(BaseModel):
    uuid: UUID


CreateEmployee.update_forward_refs()
CreateEmployeeEmployeeCreate.update_forward_refs()
