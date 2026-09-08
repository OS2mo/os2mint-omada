from typing import List
from typing import Optional
from uuid import UUID

from .base_model import BaseModel


class GetEmployeeUuidsFromItuserRelations(BaseModel):
    addresses: "GetEmployeeUuidsFromItuserRelationsAddresses"


class GetEmployeeUuidsFromItuserRelationsAddresses(BaseModel):
    objects: List["GetEmployeeUuidsFromItuserRelationsAddressesObjects"]


class GetEmployeeUuidsFromItuserRelationsAddressesObjects(BaseModel):
    validities: List["GetEmployeeUuidsFromItuserRelationsAddressesObjectsValidities"]


class GetEmployeeUuidsFromItuserRelationsAddressesObjectsValidities(BaseModel):
    person: Optional[
        List["GetEmployeeUuidsFromItuserRelationsAddressesObjectsValiditiesPerson"]
    ]


class GetEmployeeUuidsFromItuserRelationsAddressesObjectsValiditiesPerson(BaseModel):
    uuid: UUID


GetEmployeeUuidsFromItuserRelations.update_forward_refs()
GetEmployeeUuidsFromItuserRelationsAddresses.update_forward_refs()
GetEmployeeUuidsFromItuserRelationsAddressesObjects.update_forward_refs()
GetEmployeeUuidsFromItuserRelationsAddressesObjectsValidities.update_forward_refs()
GetEmployeeUuidsFromItuserRelationsAddressesObjectsValiditiesPerson.update_forward_refs()
