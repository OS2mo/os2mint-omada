# Generated by ariadne-codegen on 2024-09-09 14:40
# Source: queries.graphql

from uuid import UUID

from .base_model import BaseModel


class TestingCreateEmployee(BaseModel):
    employee_create: "TestingCreateEmployeeEmployeeCreate"


class TestingCreateEmployeeEmployeeCreate(BaseModel):
    uuid: UUID


TestingCreateEmployee.update_forward_refs()
TestingCreateEmployeeEmployeeCreate.update_forward_refs()
