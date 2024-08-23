# Generated by ariadne-codegen on 2024-08-22 18:07
# Source: queries.graphql

from typing import List
from uuid import UUID

from .base_model import BaseModel


class GetEmployeeUuidFromUserKey(BaseModel):
    engagements: "GetEmployeeUuidFromUserKeyEngagements"


class GetEmployeeUuidFromUserKeyEngagements(BaseModel):
    objects: List["GetEmployeeUuidFromUserKeyEngagementsObjects"]


class GetEmployeeUuidFromUserKeyEngagementsObjects(BaseModel):
    validities: List["GetEmployeeUuidFromUserKeyEngagementsObjectsValidities"]


class GetEmployeeUuidFromUserKeyEngagementsObjectsValidities(BaseModel):
    person: List["GetEmployeeUuidFromUserKeyEngagementsObjectsValiditiesPerson"]


class GetEmployeeUuidFromUserKeyEngagementsObjectsValiditiesPerson(BaseModel):
    uuid: UUID


GetEmployeeUuidFromUserKey.update_forward_refs()
GetEmployeeUuidFromUserKeyEngagements.update_forward_refs()
GetEmployeeUuidFromUserKeyEngagementsObjects.update_forward_refs()
GetEmployeeUuidFromUserKeyEngagementsObjectsValidities.update_forward_refs()
GetEmployeeUuidFromUserKeyEngagementsObjectsValiditiesPerson.update_forward_refs()
