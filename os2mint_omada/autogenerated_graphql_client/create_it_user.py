# Generated by ariadne-codegen on 2024-09-09 14:34
# Source: queries.graphql

from uuid import UUID

from .base_model import BaseModel


class CreateItUser(BaseModel):
    ituser_create: "CreateItUserItuserCreate"


class CreateItUserItuserCreate(BaseModel):
    uuid: UUID


CreateItUser.update_forward_refs()
CreateItUserItuserCreate.update_forward_refs()
