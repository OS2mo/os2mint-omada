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
    monkeypatch.setenv("CUSTOMER", "egedal")


@pytest.fixture
async def org_unit(graphql_client: GraphQLClient) -> str:
    # Get org unit type
    result = await graphql_client._testing__get_org_unit_type()
    org_unit_type_uuid = one(result.objects).uuid

    # Create org unit
    user_key = "Egedal Kommune"
    await graphql_client._testing__create_org_unit(
        user_key=user_key,
        org_unit_type=org_unit_type_uuid,
    )

    return user_key


@pytest.mark.integration_test
async def test_egedal_manual(
    omada_mock: Callable[[list], None],
    test_client: TestClient,
    graphql_client: GraphQLClient,
    org_unit: str,
) -> None:
    # Precondition: The person does not already exist
    cpr_number = "0902104607"
    employee = await graphql_client._testing__get_employee(cpr_number)
    assert employee.objects == []

    # CREATE
    omada_user = {
        # Omada
        "Id": 1001307,
        "UId": "93f93362-3cb4-450a-a48a-ef975675b232",
        "VALIDFROM": "2010-02-09T00:00:00+01:00",
        "VALIDTO": "2010-03-26T00:00:00+01:00",
        "IDENTITYCATEGORY": {
            "Id": 561,
            "UId": "270a1807-95ca-40b4-9ce5-475d8961f31b",
            "Value": "Contractor",
        },
        # Employee
        "C_EMPLOYEEID": cpr_number,
        "C_OIS_FIRSTNAME": "The Lich",
        "C_OIS_LASTNAME": "King",
        # Employee (manual)
        "FIRSTNAME": "Arthas",
        "LASTNAME": "Menethil",
        # Engagements (manual)
        "EMPLOYMENTS": [
            {
                "Id": 1251824,
                "UId": "0e39ce2d-39a5-42b0-befb-f8380f9c789c",
                "KeyValue": None,
                "KeyProperty": None,
                "DisplayName": f"Prince||{org_unit}||00001337;",
            },
        ],
        # Addresses
        "EMAIL": "arthas@egepost.dk",
        "PHONE": "22334455",
        # IT Users
        "OBJECTGUID": "B8-84-0B-DA-31-8E-6B-42-96-5D-0A-C0-AB-A1-D6-9F",
    }
    omada_mock([omada_user])

    test_case = unittest.TestCase()
    test_case.maxDiff = None

    @retry()
    async def verify() -> None:
        employees = await graphql_client._testing__get_employee(cpr_number)

        # Employee
        employee_states = one(employees.objects)
        employee = one(employee_states.objects)
        assert employee.cpr_number == cpr_number
        assert employee.given_name == "Arthas"
        assert employee.surname == "Menethil"
        assert employee.nickname_given_name == "The Lich"
        assert employee.nickname_surname == "King"
        assert employee.validity.from_ == datetime(
            2010, 2, 9, 0, 0, tzinfo=timezone(timedelta(hours=1))
        )
        assert employee.validity.to is None

        # Engagement
        test_case.assertCountEqual(
            [e.dict() for e in employee.engagements],
            [
                {
                    "user_key": "1337",
                    "org_unit": [{"user_key": "Egedal Kommune"}],
                    "job_function": {"user_key": "not_applicable"},
                    "engagement_type": {"user_key": "omada_manually_created"},
                    "primary": {"user_key": "primary"},
                    "validity": {
                        "from_": datetime(
                            2010, 2, 9, 0, 0, tzinfo=timezone(timedelta(hours=1))
                        ),
                        "to": datetime(
                            2010, 3, 26, 0, 0, tzinfo=timezone(timedelta(hours=1))
                        ),
                    },
                },
            ],
        )

        # Addresses
        test_case.assertCountEqual(
            [a.dict() for a in employee.addresses],
            [
                {
                    "value": "22334455",
                    "address_type": {"user_key": "OmadaPhoneEmployee"},
                    "engagement": None,
                    "visibility": {"user_key": "Public"},
                    "validity": {
                        "from_": datetime(
                            2010, 2, 9, 0, 0, tzinfo=timezone(timedelta(hours=1))
                        ),
                        "to": datetime(
                            2010, 3, 26, 0, 0, tzinfo=timezone(timedelta(hours=1))
                        ),
                    },
                },
                {
                    "value": "arthas@egepost.dk",
                    "address_type": {"user_key": "OmadaEmailEmployee"},
                    "engagement": None,
                    "visibility": {"user_key": "Public"},
                    "validity": {
                        "from_": datetime(
                            2010, 2, 9, 0, 0, tzinfo=timezone(timedelta(hours=1))
                        ),
                        "to": datetime(
                            2010, 3, 26, 0, 0, tzinfo=timezone(timedelta(hours=1))
                        ),
                    },
                },
            ],
        )

        # IT Users
        test_case.assertCountEqual(
            [u.dict() for u in employee.itusers],
            [
                {
                    "user_key": "da0b84b8-8e31-426b-965d-0ac0aba1d69f",
                    "itsystem": {"user_key": "omada_ad_guid"},
                    "engagement": None,
                    "validity": {
                        "from_": datetime(
                            2010, 2, 9, 0, 0, tzinfo=timezone(timedelta(hours=1))
                        ),
                        "to": datetime(
                            2010, 3, 26, 0, 0, tzinfo=timezone(timedelta(hours=1))
                        ),
                    },
                }
            ],
        )

    await verify()

    # EDIT
    updated_omada_user = {
        **omada_user,
        # Employee
        "C_OIS_FIRSTNAME": "Mr M.",
        # Employee (manual)
        "FIRSTNAME": "The King",
        # Engagements (manual)
        "EMPLOYMENTS": omada_user["EMPLOYMENTS"]
        + [  # type: ignore[operator]
            {
                "Id": 6849240,
                "UId": "7884a4f1-948c-460a-9cc7-47bdc031d841",
                "KeyValue": None,
                "KeyProperty": None,
                "DisplayName": f"Sygeplejerske||{org_unit}||00001234;",
            },
        ],
        # Addresses
        "EMAIL": "thelichking@egepost.dk",
        "PHONE": None,  # deleted
        "CELLPHONE": "55443322",
        # IT Users
        "OBJECTGUID": "11-22-33-44-55-66-77-88-99-00-AA-BB-CC-DD-EE-FF",
        "C_ADUSERNAME": "LK1337",
    }
    omada_mock([updated_omada_user])

    @retry()
    async def verify() -> None:
        employees = await graphql_client._testing__get_employee(cpr_number)

        # Employee
        employee_states = one(employees.objects)
        employee = one(employee_states.objects)
        assert employee.given_name == "The King"
        assert employee.nickname_given_name == "Mr M."

        # Engagement
        test_case.assertCountEqual(
            [e.dict() for e in employee.engagements],
            [
                {
                    "user_key": "1337",
                    "org_unit": [{"user_key": "Egedal Kommune"}],
                    "job_function": {"user_key": "not_applicable"},
                    "engagement_type": {"user_key": "omada_manually_created"},
                    "primary": {"user_key": "primary"},
                    "validity": {
                        "from_": datetime(
                            2010, 2, 9, 0, 0, tzinfo=timezone(timedelta(hours=1))
                        ),
                        "to": datetime(
                            2010, 3, 26, 0, 0, tzinfo=timezone(timedelta(hours=1))
                        ),
                    },
                },
                {
                    "user_key": "1234",
                    "org_unit": [{"user_key": "Egedal Kommune"}],
                    "job_function": {"user_key": "Sygeplejerske"},
                    "engagement_type": {"user_key": "omada_manually_created"},
                    "primary": {"user_key": "primary"},
                    "validity": {
                        "from_": datetime(
                            2010, 2, 9, 0, 0, tzinfo=timezone(timedelta(hours=1))
                        ),
                        "to": datetime(
                            2010, 3, 26, 0, 0, tzinfo=timezone(timedelta(hours=1))
                        ),
                    },
                },
            ],
        )

        # Addresses
        assert {a.value for a in employee.addresses} == {
            "thelichking@egepost.dk",
            "55443322",
        }

        # IT Users
        assert {u.user_key for u in employee.itusers} == {
            "44332211-6655-8877-9900-aabbccddeeff",
            "LK1337",
        }

    await verify()

    # DELETE
    omada_mock([])

    @retry()
    async def verify() -> None:
        employees = await graphql_client._testing__get_employee(cpr_number)
        employee_states = one(employees.objects)
        employee = one(employee_states.objects)
        assert employee.engagements == []
        assert employee.addresses == []
        assert employee.itusers == []

    await verify()
