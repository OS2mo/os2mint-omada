# Generated by ariadne-codegen on 2024-10-10 13:36
# Source: queries.graphql

from typing import Any
from typing import List
from typing import Optional
from typing import Union
from uuid import UUID

from ._testing__create_employee import TestingCreateEmployee
from ._testing__create_employee import TestingCreateEmployeeEmployeeCreate
from ._testing__create_org_unit import TestingCreateOrgUnit
from ._testing__create_org_unit import TestingCreateOrgUnitOrgUnitCreate
from ._testing__create_org_unit_it_user import TestingCreateOrgUnitItUser
from ._testing__create_org_unit_it_user import TestingCreateOrgUnitItUserItuserCreate
from ._testing__get_employee import TestingGetEmployee
from ._testing__get_employee import TestingGetEmployeeEmployees
from ._testing__get_it_system import TestingGetItSystem
from ._testing__get_it_system import TestingGetItSystemItsystems
from ._testing__get_org_unit_type import TestingGetOrgUnitType
from ._testing__get_org_unit_type import TestingGetOrgUnitTypeClasses
from .async_base_client import AsyncBaseClient
from .base_model import UNSET
from .base_model import UnsetType
from .create_address import CreateAddress
from .create_address import CreateAddressAddressCreate
from .create_employee import CreateEmployee
from .create_employee import CreateEmployeeEmployeeCreate
from .create_engagement import CreateEngagement
from .create_engagement import CreateEngagementEngagementCreate
from .create_it_user import CreateItUser
from .create_it_user import CreateItUserItuserCreate
from .delete_address import DeleteAddress
from .delete_address import DeleteAddressAddressDelete
from .delete_engagement import DeleteEngagement
from .delete_engagement import DeleteEngagementEngagementDelete
from .delete_it_user import DeleteItUser
from .delete_it_user import DeleteItUserItuserDelete
from .get_classes import GetClasses
from .get_classes import GetClassesFacets
from .get_current_employee_state import GetCurrentEmployeeState
from .get_current_employee_state import GetCurrentEmployeeStateEmployees
from .get_employee_addresses import GetEmployeeAddresses
from .get_employee_addresses import GetEmployeeAddressesEmployees
from .get_employee_engagements import GetEmployeeEngagements
from .get_employee_engagements import GetEmployeeEngagementsEmployees
from .get_employee_it_users import GetEmployeeItUsers
from .get_employee_it_users import GetEmployeeItUsersEmployees
from .get_employee_states import GetEmployeeStates
from .get_employee_states import GetEmployeeStatesEmployees
from .get_employee_uuid_from_cpr import GetEmployeeUuidFromCpr
from .get_employee_uuid_from_cpr import GetEmployeeUuidFromCprEmployees
from .get_employee_uuid_from_user_key import GetEmployeeUuidFromUserKey
from .get_employee_uuid_from_user_key import GetEmployeeUuidFromUserKeyEngagements
from .get_it_systems import GetItSystems
from .get_it_systems import GetItSystemsItsystems
from .get_org_unit_validity import GetOrgUnitValidity
from .get_org_unit_validity import GetOrgUnitValidityOrgUnits
from .get_org_unit_with_it_system_user_key import GetOrgUnitWithItSystemUserKey
from .get_org_unit_with_it_system_user_key import GetOrgUnitWithItSystemUserKeyItusers
from .get_org_unit_with_user_key import GetOrgUnitWithUserKey
from .get_org_unit_with_user_key import GetOrgUnitWithUserKeyOrgUnits
from .get_org_unit_with_uuid import GetOrgUnitWithUuid
from .get_org_unit_with_uuid import GetOrgUnitWithUuidOrgUnits
from .input_types import AddressCreateInput
from .input_types import EmployeeCreateInput
from .input_types import EngagementCreateInput
from .input_types import ITUserCreateInput


def gql(q: str) -> str:
    return q


class GraphQLClient(AsyncBaseClient):
    async def get_it_systems(
        self, user_keys: Union[Optional[List[str]], UnsetType] = UNSET
    ) -> GetItSystemsItsystems:
        query = gql(
            """
            query get_it_systems($user_keys: [String!]) {
              itsystems(filter: {user_keys: $user_keys}) {
                objects {
                  current {
                    uuid
                    user_key
                  }
                }
              }
            }
            """
        )
        variables: dict[str, object] = {"user_keys": user_keys}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetItSystems.parse_obj(data).itsystems

    async def get_classes(
        self, user_keys: Union[Optional[List[str]], UnsetType] = UNSET
    ) -> GetClassesFacets:
        query = gql(
            """
            query get_classes($user_keys: [String!]) {
              facets(filter: {user_keys: $user_keys}) {
                objects {
                  current {
                    classes {
                      uuid
                      user_key
                    }
                  }
                }
              }
            }
            """
        )
        variables: dict[str, object] = {"user_keys": user_keys}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetClasses.parse_obj(data).facets

    async def get_employee_uuid_from_user_key(
        self, user_keys: Union[Optional[List[str]], UnsetType] = UNSET
    ) -> GetEmployeeUuidFromUserKeyEngagements:
        query = gql(
            """
            query get_employee_uuid_from_user_key($user_keys: [String!]) {
              engagements(filter: {user_keys: $user_keys, from_date: null, to_date: null}) {
                objects {
                  validities(start: null, end: null) {
                    person(filter: {from_date: null, to_date: null}) {
                      uuid
                    }
                  }
                }
              }
            }
            """
        )
        variables: dict[str, object] = {"user_keys": user_keys}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetEmployeeUuidFromUserKey.parse_obj(data).engagements

    async def get_employee_uuid_from_cpr(
        self, cpr_numbers: Union[Optional[List[Any]], UnsetType] = UNSET
    ) -> GetEmployeeUuidFromCprEmployees:
        query = gql(
            """
            query get_employee_uuid_from_cpr($cpr_numbers: [CPR!]) {
              employees(filter: {cpr_numbers: $cpr_numbers, from_date: null, to_date: null}) {
                objects {
                  uuid
                }
              }
            }
            """
        )
        variables: dict[str, object] = {"cpr_numbers": cpr_numbers}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetEmployeeUuidFromCpr.parse_obj(data).employees

    async def get_employee_states(
        self, uuids: Union[Optional[List[UUID]], UnsetType] = UNSET
    ) -> GetEmployeeStatesEmployees:
        query = gql(
            """
            query get_employee_states($uuids: [UUID!]) {
              employees(filter: {uuids: $uuids, from_date: null, to_date: null}) {
                objects {
                  validities(start: null, end: null) {
                    uuid
                    given_name
                    surname
                    nickname_given_name
                    nickname_surname
                    cpr_number
                  }
                }
              }
            }
            """
        )
        variables: dict[str, object] = {"uuids": uuids}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetEmployeeStates.parse_obj(data).employees

    async def get_current_employee_state(
        self, uuids: Union[Optional[List[UUID]], UnsetType] = UNSET
    ) -> GetCurrentEmployeeStateEmployees:
        query = gql(
            """
            query get_current_employee_state($uuids: [UUID!]) {
              employees(filter: {uuids: $uuids}) {
                objects {
                  current {
                    uuid
                    given_name
                    surname
                    nickname_given_name
                    nickname_surname
                    cpr_number
                    seniority
                  }
                }
              }
            }
            """
        )
        variables: dict[str, object] = {"uuids": uuids}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetCurrentEmployeeState.parse_obj(data).employees

    async def get_employee_addresses(
        self,
        employee_uuids: Union[Optional[List[UUID]], UnsetType] = UNSET,
        address_types: Union[Optional[List[UUID]], UnsetType] = UNSET,
    ) -> GetEmployeeAddressesEmployees:
        query = gql(
            """
            query get_employee_addresses($employee_uuids: [UUID!], $address_types: [UUID!]) {
              employees(filter: {uuids: $employee_uuids, from_date: null, to_date: null}) {
                objects {
                  validities(start: null, end: null) {
                    addresses(
                      filter: {address_types: $address_types, from_date: null, to_date: null}
                    ) {
                      uuid
                      value
                      address_type(filter: {from_date: null, to_date: null}) {
                        uuid
                      }
                      person(filter: {from_date: null, to_date: null}) {
                        uuid
                      }
                      engagement(filter: {from_date: null, to_date: null}) {
                        uuid
                      }
                      ituser(filter: {from_date: null, to_date: null}) {
                        uuid
                      }
                      visibility(filter: {from_date: null, to_date: null}) {
                        uuid
                      }
                      validity {
                        from
                        to
                      }
                    }
                  }
                }
              }
            }
            """
        )
        variables: dict[str, object] = {
            "employee_uuids": employee_uuids,
            "address_types": address_types,
        }
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetEmployeeAddresses.parse_obj(data).employees

    async def get_employee_engagements(
        self, employee_uuids: Union[Optional[List[UUID]], UnsetType] = UNSET
    ) -> GetEmployeeEngagementsEmployees:
        query = gql(
            """
            query get_employee_engagements($employee_uuids: [UUID!]) {
              employees(filter: {uuids: $employee_uuids, from_date: null, to_date: null}) {
                objects {
                  validities(start: null, end: null) {
                    engagements(filter: {from_date: null, to_date: null}) {
                      uuid
                      user_key
                      org_unit(filter: {from_date: null, to_date: null}) {
                        uuid
                      }
                      person(filter: {from_date: null, to_date: null}) {
                        uuid
                      }
                      job_function(filter: {from_date: null, to_date: null}) {
                        uuid
                      }
                      engagement_type(filter: {from_date: null, to_date: null}) {
                        uuid
                      }
                      primary(filter: {from_date: null, to_date: null}) {
                        uuid
                      }
                      validity {
                        from
                        to
                      }
                    }
                  }
                }
              }
            }
            """
        )
        variables: dict[str, object] = {"employee_uuids": employee_uuids}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetEmployeeEngagements.parse_obj(data).employees

    async def get_employee_it_users(
        self,
        employee_uuids: Union[Optional[List[UUID]], UnsetType] = UNSET,
        it_system_uuids: Union[Optional[List[UUID]], UnsetType] = UNSET,
    ) -> GetEmployeeItUsersEmployees:
        query = gql(
            """
            query get_employee_it_users($employee_uuids: [UUID!], $it_system_uuids: [UUID!]) {
              employees(filter: {uuids: $employee_uuids, from_date: null, to_date: null}) {
                objects {
                  validities(start: null, end: null) {
                    itusers(
                      filter: {from_date: null, to_date: null, itsystem: {uuids: $it_system_uuids}}
                    ) {
                      uuid
                      external_id
                      user_key
                      itsystem(filter: {from_date: null, to_date: null}) {
                        uuid
                      }
                      person(filter: {from_date: null, to_date: null}) {
                        uuid
                      }
                      engagement(filter: {from_date: null, to_date: null}) {
                        uuid
                      }
                      validity {
                        from
                        to
                      }
                    }
                  }
                }
              }
            }
            """
        )
        variables: dict[str, object] = {
            "employee_uuids": employee_uuids,
            "it_system_uuids": it_system_uuids,
        }
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetEmployeeItUsers.parse_obj(data).employees

    async def get_org_unit_with_it_system_user_key(
        self, user_keys: Union[Optional[List[str]], UnsetType] = UNSET
    ) -> GetOrgUnitWithItSystemUserKeyItusers:
        query = gql(
            """
            query get_org_unit_with_it_system_user_key($user_keys: [String!]) {
              itusers(filter: {user_keys: $user_keys, from_date: null, to_date: null}) {
                objects {
                  validities(start: null, end: null) {
                    org_unit(filter: {from_date: null, to_date: null}) {
                      uuid
                    }
                  }
                }
              }
            }
            """
        )
        variables: dict[str, object] = {"user_keys": user_keys}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetOrgUnitWithItSystemUserKey.parse_obj(data).itusers

    async def get_org_unit_with_uuid(
        self, uuids: Union[Optional[List[UUID]], UnsetType] = UNSET
    ) -> GetOrgUnitWithUuidOrgUnits:
        query = gql(
            """
            query get_org_unit_with_uuid($uuids: [UUID!]) {
              org_units(filter: {uuids: $uuids, from_date: null, to_date: null}) {
                objects {
                  uuid
                }
              }
            }
            """
        )
        variables: dict[str, object] = {"uuids": uuids}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetOrgUnitWithUuid.parse_obj(data).org_units

    async def get_org_unit_with_user_key(
        self, user_keys: Union[Optional[List[str]], UnsetType] = UNSET
    ) -> GetOrgUnitWithUserKeyOrgUnits:
        query = gql(
            """
            query get_org_unit_with_user_key($user_keys: [String!]) {
              org_units(filter: {user_keys: $user_keys, from_date: null, to_date: null}) {
                objects {
                  uuid
                }
              }
            }
            """
        )
        variables: dict[str, object] = {"user_keys": user_keys}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetOrgUnitWithUserKey.parse_obj(data).org_units

    async def get_org_unit_validity(
        self, uuids: Union[Optional[List[UUID]], UnsetType] = UNSET
    ) -> GetOrgUnitValidityOrgUnits:
        query = gql(
            """
            query get_org_unit_validity($uuids: [UUID!]) {
              org_units(filter: {uuids: $uuids, from_date: null, to_date: null}) {
                objects {
                  validities(start: null, end: null) {
                    validity {
                      from_date: from
                      to_date: to
                    }
                  }
                }
              }
            }
            """
        )
        variables: dict[str, object] = {"uuids": uuids}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetOrgUnitValidity.parse_obj(data).org_units

    async def create_address(
        self, input: AddressCreateInput
    ) -> CreateAddressAddressCreate:
        query = gql(
            """
            mutation create_address($input: AddressCreateInput!) {
              address_create(input: $input) {
                uuid
              }
            }
            """
        )
        variables: dict[str, object] = {"input": input}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return CreateAddress.parse_obj(data).address_create

    async def create_employee(
        self, input: EmployeeCreateInput
    ) -> CreateEmployeeEmployeeCreate:
        query = gql(
            """
            mutation create_employee($input: EmployeeCreateInput!) {
              employee_create(input: $input) {
                uuid
              }
            }
            """
        )
        variables: dict[str, object] = {"input": input}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return CreateEmployee.parse_obj(data).employee_create

    async def create_engagement(
        self, input: EngagementCreateInput
    ) -> CreateEngagementEngagementCreate:
        query = gql(
            """
            mutation create_engagement($input: EngagementCreateInput!) {
              engagement_create(input: $input) {
                uuid
              }
            }
            """
        )
        variables: dict[str, object] = {"input": input}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return CreateEngagement.parse_obj(data).engagement_create

    async def create_it_user(
        self, input: ITUserCreateInput
    ) -> CreateItUserItuserCreate:
        query = gql(
            """
            mutation create_it_user($input: ITUserCreateInput!) {
              ituser_create(input: $input) {
                uuid
              }
            }
            """
        )
        variables: dict[str, object] = {"input": input}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return CreateItUser.parse_obj(data).ituser_create

    async def delete_address(self, uuid: UUID) -> DeleteAddressAddressDelete:
        query = gql(
            """
            mutation delete_address($uuid: UUID!) {
              address_delete(uuid: $uuid) {
                uuid
              }
            }
            """
        )
        variables: dict[str, object] = {"uuid": uuid}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return DeleteAddress.parse_obj(data).address_delete

    async def delete_engagement(self, uuid: UUID) -> DeleteEngagementEngagementDelete:
        query = gql(
            """
            mutation delete_engagement($uuid: UUID!) {
              engagement_delete(uuid: $uuid) {
                uuid
              }
            }
            """
        )
        variables: dict[str, object] = {"uuid": uuid}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return DeleteEngagement.parse_obj(data).engagement_delete

    async def delete_it_user(self, uuid: UUID) -> DeleteItUserItuserDelete:
        query = gql(
            """
            mutation delete_it_user($uuid: UUID!) {
              ituser_delete(uuid: $uuid) {
                uuid
              }
            }
            """
        )
        variables: dict[str, object] = {"uuid": uuid}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return DeleteItUser.parse_obj(data).ituser_delete

    async def _testing__get_employee(
        self, cpr_number: Any
    ) -> TestingGetEmployeeEmployees:
        query = gql(
            """
            query _Testing_GetEmployee($cpr_number: CPR!) {
              employees(filter: {cpr_numbers: [$cpr_number], from_date: null, to_date: null}) {
                objects {
                  validities(start: null, end: null) {
                    cpr_number
                    given_name
                    surname
                    nickname_given_name
                    nickname_surname
                    validity {
                      from
                      to
                    }
                    engagements(filter: {from_date: null, to_date: null}) {
                      user_key
                      org_unit(filter: {from_date: null, to_date: null}) {
                        user_key
                      }
                      job_function(filter: {from_date: null, to_date: null}) {
                        user_key
                      }
                      engagement_type(filter: {from_date: null, to_date: null}) {
                        user_key
                      }
                      primary(filter: {from_date: null, to_date: null}) {
                        user_key
                      }
                      validity {
                        from
                        to
                      }
                    }
                    addresses(filter: {from_date: null, to_date: null}) {
                      value
                      address_type(filter: {from_date: null, to_date: null}) {
                        user_key
                      }
                      engagement(filter: {from_date: null, to_date: null}) {
                        user_key
                      }
                      ituser(filter: {from_date: null, to_date: null}) {
                        user_key
                      }
                      visibility(filter: {from_date: null, to_date: null}) {
                        user_key
                      }
                      validity {
                        from
                        to
                      }
                    }
                    itusers(filter: {from_date: null, to_date: null}) {
                      external_id
                      user_key
                      itsystem(filter: {from_date: null, to_date: null}) {
                        user_key
                      }
                      engagement(filter: {from_date: null, to_date: null}) {
                        user_key
                      }
                      validity {
                        from
                        to
                      }
                    }
                  }
                }
              }
            }
            """
        )
        variables: dict[str, object] = {"cpr_number": cpr_number}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingGetEmployee.parse_obj(data).employees

    async def _testing__create_employee(
        self,
        cpr_number: Any,
        given_name: str,
        surname: str,
        nickname_given_name: Union[Optional[str], UnsetType] = UNSET,
        nickname_surname: Union[Optional[str], UnsetType] = UNSET,
    ) -> TestingCreateEmployeeEmployeeCreate:
        query = gql(
            """
            mutation _Testing_CreateEmployee($cpr_number: CPR!, $given_name: String!, $surname: String!, $nickname_given_name: String = null, $nickname_surname: String = null) {
              employee_create(
                input: {cpr_number: $cpr_number, given_name: $given_name, surname: $surname, nickname_given_name: $nickname_given_name, nickname_surname: $nickname_surname}
              ) {
                uuid
              }
            }
            """
        )
        variables: dict[str, object] = {
            "cpr_number": cpr_number,
            "given_name": given_name,
            "surname": surname,
            "nickname_given_name": nickname_given_name,
            "nickname_surname": nickname_surname,
        }
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingCreateEmployee.parse_obj(data).employee_create

    async def _testing__get_org_unit_type(self) -> TestingGetOrgUnitTypeClasses:
        query = gql(
            """
            query _Testing_GetOrgUnitType {
              classes(filter: {facet: {user_keys: "org_unit_type"}, user_keys: "Afdeling"}) {
                objects {
                  uuid
                }
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingGetOrgUnitType.parse_obj(data).classes

    async def _testing__create_org_unit(
        self, user_key: str, org_unit_type: UUID
    ) -> TestingCreateOrgUnitOrgUnitCreate:
        query = gql(
            """
            mutation _Testing_CreateOrgUnit($user_key: String!, $org_unit_type: UUID!) {
              org_unit_create(
                input: {name: "Test Org Unit", user_key: $user_key, org_unit_type: $org_unit_type, validity: {from: "2010-02-03"}}
              ) {
                uuid
              }
            }
            """
        )
        variables: dict[str, object] = {
            "user_key": user_key,
            "org_unit_type": org_unit_type,
        }
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingCreateOrgUnit.parse_obj(data).org_unit_create

    async def _testing__get_it_system(
        self, user_key: str
    ) -> TestingGetItSystemItsystems:
        query = gql(
            """
            query _Testing_GetItSystem($user_key: String!) {
              itsystems(filter: {user_keys: [$user_key]}) {
                objects {
                  uuid
                }
              }
            }
            """
        )
        variables: dict[str, object] = {"user_key": user_key}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingGetItSystem.parse_obj(data).itsystems

    async def _testing__create_org_unit_it_user(
        self, user_key: str, it_system: UUID, org_unit: UUID
    ) -> TestingCreateOrgUnitItUserItuserCreate:
        query = gql(
            """
            mutation _Testing_CreateOrgUnitItUser($user_key: String!, $it_system: UUID!, $org_unit: UUID!) {
              ituser_create(
                input: {user_key: $user_key, itsystem: $it_system, org_unit: $org_unit, validity: {from: "2010-02-03"}}
              ) {
                uuid
              }
            }
            """
        )
        variables: dict[str, object] = {
            "user_key": user_key,
            "it_system": it_system,
            "org_unit": org_unit,
        }
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingCreateOrgUnitItUser.parse_obj(data).ituser_create
