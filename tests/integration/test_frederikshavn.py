# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# mypy: disable-error-code="no-redef"
import unittest
from collections.abc import Callable
from datetime import datetime
from datetime import timedelta
from datetime import timezone

import pytest
from fastapi.testclient import TestClient
from more_itertools import one
from pytest import MonkeyPatch

from os2mint_omada.autogenerated_graphql_client import GraphQLClient
from tests.integration.util import retry


# TODO: Test moving org unit


@pytest.fixture(autouse=True)
def set_customer(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("CUSTOMER", "frederikshavn")


@pytest.fixture
async def org_unit(graphql_client: GraphQLClient) -> str:
    # Get org unit type
    result = await graphql_client._testing__get_org_unit_type()
    org_unit_type_uuid = one(result.objects).uuid

    # Create org unit
    user_key = "1012415"
    await graphql_client._testing__create_org_unit(
        user_key=user_key,
        org_unit_type=org_unit_type_uuid,
    )

    return user_key


@pytest.mark.integration_test
async def test_frederikshavn(
    omada_mock: Callable[[list], None],
    test_client: TestClient,
    graphql_client: GraphQLClient,
    org_unit: str,
) -> None:
    # Precondition: The person does not already exist
    cpr_number = "0706994939"
    employee = await graphql_client._testing__employee_query(cpr_number)
    assert employee.objects == []

    # CREATE
    omada_user = {
        # Omada
        "Id": "1277266",
        "UId": "347a7d7a-49d6-4e90-93c8-88f3a0a40548",
        "VALIDFROM": "2021-01-31T08:44:00+01:00",
        "VALIDTO": "9999-12-31T00:00:00+01:00",
        "IDENTITYCATEGORY": {
            "Id": "1000245",
            "UId": "7e7b6153-539d-459a-b47b-2500ddb76543",
        },
        # Employee
        "FIRSTNAME": "Villads",
        "LASTNAME": "Vikar",
        "C_CPRNUMBER": "070699-4939",
        # Engagement
        "C_MEDARBEJDERNR_ODATA": "1337007",
        "C_JOBTITLE_ODATA": "Vikar",
        "C_OUID_ODATA": "01012415",
        # IT Users
        "ADLOGON": "VIVI04",
        # Addresses
        "EMAIL": "VIVI04@frederikshavn.dk",
        "C_TELEPHONENUMBER": "+45 12 31 32 12",
        "CELLPHONE": "12345678",
    }
    omada_mock([omada_user])

    test_case = unittest.TestCase()
    test_case.maxDiff = None

    @retry()
    async def verify() -> None:
        employees = await graphql_client._testing__employee_query(cpr_number)

        # Employee
        employee_states = one(employees.objects)
        employee = one(employee_states.objects)
        assert employee.cpr_number == cpr_number
        assert employee.given_name == "Villads"
        assert employee.surname == "Vikar"
        assert employee.validity.from_ == datetime(
            1999, 6, 7, 0, 0, tzinfo=timezone(timedelta(hours=2))
        )
        assert employee.validity.to is None

        # Engagement
        test_case.assertCountEqual(
            [e.dict() for e in employee.engagements],
            [
                {
                    "user_key": "1337007",
                    "org_unit": [{"user_key": "1012415"}],
                    "job_function": {"user_key": "Vikar"},
                    "engagement_type": {"user_key": "omada_manually_created"},
                    "primary": {"user_key": "primary"},
                    "validity": {
                        "from_": datetime(
                            2021, 1, 31, 0, 0, tzinfo=timezone(timedelta(hours=1))
                        ),
                        "to": None,
                    },
                }
            ],
        )

        # Addresses
        test_case.assertCountEqual(
            [a.dict() for a in employee.addresses],
            [
                {
                    "value": "+4512313212",
                    "address_type": {"user_key": "OmadaPhoneEmployee"},
                    "engagement": [{"user_key": "1337007"}],
                    "visibility": {"user_key": "Public"},
                    "validity": {
                        "from_": datetime(
                            2021, 1, 31, 0, 0, tzinfo=timezone(timedelta(hours=1))
                        ),
                        "to": None,
                    },
                },
                {
                    "value": "12345678",
                    "address_type": {"user_key": "OmadaMobilePhoneEmployee"},
                    "engagement": [{"user_key": "1337007"}],
                    "visibility": {"user_key": "Public"},
                    "validity": {
                        "from_": datetime(
                            2021, 1, 31, 0, 0, tzinfo=timezone(timedelta(hours=1))
                        ),
                        "to": None,
                    },
                },
                {
                    "value": "VIVI04@frederikshavn.dk",
                    "address_type": {"user_key": "OmadaEmailEmployee"},
                    "engagement": [
                        {"user_key": "1337007"},
                    ],
                    "visibility": {"user_key": "Public"},
                    "validity": {
                        "from_": datetime(
                            2021, 1, 31, 0, 0, tzinfo=timezone(timedelta(hours=1))
                        ),
                        "to": None,
                    },
                },
            ],
        )

        # IT Users
        test_case.assertCountEqual(
            [u.dict() for u in employee.itusers],
            [
                {
                    "user_key": "VIVI04",
                    "itsystem": {"user_key": "omada_ad_login"},
                    "engagement": [{"user_key": "1337007"}],
                    "validity": {
                        "from_": datetime(
                            2021, 1, 31, 0, 0, tzinfo=timezone(timedelta(hours=1))
                        ),
                        "to": None,
                    },
                }
            ],
        )

    await verify()

    # EDIT
    updated_omada_user = {
        **omada_user,
        "FIRSTNAME": "Leonardo",
        "C_MEDARBEJDERNR_ODATA": "1337420",
        "C_JOBTITLE_ODATA": "Something That Doesn't Exist in MO",
        "ADLOGON": "LEO42",
        "EMAIL": "LEO42@frederikshavn.dk",
        "C_TELEPHONENUMBER": "",  # deleted
    }
    omada_mock([updated_omada_user])

    @retry()
    async def verify() -> None:
        employees = await graphql_client._testing__employee_query(cpr_number)

        # Employee
        employee_states = one(employees.objects)
        employee = one(employee_states.objects)
        assert employee.given_name == "Leonardo"

        # Engagement
        test_case.assertCountEqual(
            [e.dict() for e in employee.engagements],
            [
                {
                    "user_key": "1337420",
                    "org_unit": [{"user_key": "1012415"}],
                    "job_function": {"user_key": "not_applicable"},
                    "engagement_type": {"user_key": "omada_manually_created"},
                    "primary": {"user_key": "primary"},
                    "validity": {
                        "from_": datetime(
                            2021, 1, 31, 0, 0, tzinfo=timezone(timedelta(hours=1))
                        ),
                        "to": None,
                    },
                }
            ],
        )

        # Addresses
        assert {a.value for a in employee.addresses} == {
            "LEO42@frederikshavn.dk",
            "12345678",
        }

        # IT Users
        assert {u.user_key for u in employee.itusers} == {
            "LEO42",
        }

    await verify()

    # DELETE
    omada_mock([])

    @retry()
    async def verify() -> None:
        employees = await graphql_client._testing__employee_query(cpr_number)
        employee_states = one(employees.objects)
        employee = one(employee_states.objects)
        assert employee.engagements == []
        assert employee.addresses == []
        assert employee.itusers == []

    await verify()
