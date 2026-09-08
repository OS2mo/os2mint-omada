from typing import List
from typing import Optional
from uuid import UUID

from .base_model import BaseModel


class GetEmployeeUuidsFromEngagementRelations(BaseModel):
    itusers: "GetEmployeeUuidsFromEngagementRelationsItusers"
    addresses: "GetEmployeeUuidsFromEngagementRelationsAddresses"


class GetEmployeeUuidsFromEngagementRelationsItusers(BaseModel):
    objects: List["GetEmployeeUuidsFromEngagementRelationsItusersObjects"]


class GetEmployeeUuidsFromEngagementRelationsItusersObjects(BaseModel):
    validities: List["GetEmployeeUuidsFromEngagementRelationsItusersObjectsValidities"]


class GetEmployeeUuidsFromEngagementRelationsItusersObjectsValidities(BaseModel):
    person: Optional[
        List["GetEmployeeUuidsFromEngagementRelationsItusersObjectsValiditiesPerson"]
    ]


class GetEmployeeUuidsFromEngagementRelationsItusersObjectsValiditiesPerson(BaseModel):
    uuid: UUID


class GetEmployeeUuidsFromEngagementRelationsAddresses(BaseModel):
    objects: List["GetEmployeeUuidsFromEngagementRelationsAddressesObjects"]


class GetEmployeeUuidsFromEngagementRelationsAddressesObjects(BaseModel):
    validities: List[
        "GetEmployeeUuidsFromEngagementRelationsAddressesObjectsValidities"
    ]


class GetEmployeeUuidsFromEngagementRelationsAddressesObjectsValidities(BaseModel):
    person: Optional[
        List["GetEmployeeUuidsFromEngagementRelationsAddressesObjectsValiditiesPerson"]
    ]


class GetEmployeeUuidsFromEngagementRelationsAddressesObjectsValiditiesPerson(
    BaseModel
):
    uuid: UUID


GetEmployeeUuidsFromEngagementRelations.update_forward_refs()
GetEmployeeUuidsFromEngagementRelationsItusers.update_forward_refs()
GetEmployeeUuidsFromEngagementRelationsItusersObjects.update_forward_refs()
GetEmployeeUuidsFromEngagementRelationsItusersObjectsValidities.update_forward_refs()
GetEmployeeUuidsFromEngagementRelationsItusersObjectsValiditiesPerson.update_forward_refs()
GetEmployeeUuidsFromEngagementRelationsAddresses.update_forward_refs()
GetEmployeeUuidsFromEngagementRelationsAddressesObjects.update_forward_refs()
GetEmployeeUuidsFromEngagementRelationsAddressesObjectsValidities.update_forward_refs()
GetEmployeeUuidsFromEngagementRelationsAddressesObjectsValiditiesPerson.update_forward_refs()
