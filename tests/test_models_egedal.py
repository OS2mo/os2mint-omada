# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from uuid import UUID

import pytest

from os2mint_omada.sync.egedal.models import EgedalOmadaEmployment
from os2mint_omada.sync.egedal.models import EgedalOmadaUser
from os2mint_omada.sync.egedal.models import ManualEgedalOmadaUser


@pytest.fixture
def egedal_omada_user() -> dict:
    """Egedal Omada user, as returned by the API."""
    return {
        # Omada
        "Id": 1001378,
        "UId": "ae2923ea-2fb4-44bc-91b8-237a1ca5ee61",
        "VALIDFROM": "2002-07-03T00:00:00+02:00",
        "VALIDTO": "2003-07-01T00:00:00+01:00",
        "IDENTITYCATEGORY": {
            "Id": 560,
            "UId": "ac0c67fc-5f47-4112-94e6-446bfb68326a",
            "Value": "Employee",
        },
        # Employee
        "C_EMPLOYEEID": "0307024004",
        "C_OIS_FIRSTNAME": "Jaina",
        "C_OIS_LASTNAME": "Proudmoore",
        # Addresses
        "EMAIL": "jaina@egepost.dk",
        "PHONE": "12345678",
        "CELLPHONE": "87654321",
        # IT Users
        "OBJECTGUID": "C2-2C-C1-C7-45-E8-83-49-85-4F-DA-EF-0B-32-B8-78",
        "C_ADUSERNAME": "JP1911",
    }


@pytest.fixture
def manual_egedal_omada_user() -> dict:
    """Manual Egedal Omada user, as returned by the API."""
    return {
        # Omada
        "Id": 1001307,
        "UId": "93f93362-3cb4-450a-a48a-ef975675b232",
        "VALIDFROM": "2010-02-09T00:00:00+02:00",
        "VALIDTO": "2010-03-26T00:00:00+01:00",
        "IDENTITYCATEGORY": {
            "Id": 561,
            "UId": "270a1807-95ca-40b4-9ce5-475d8961f31b",
            "Value": "Contractor",
        },
        # Employee
        "C_EMPLOYEEID": "0902104607",
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
                "DisplayName": "Prince (Lordaeron [LORDAERON]) ID:(00001337) ;",
            },
            {
                "Id": 6849240,
                "UId": "7884a4f1-948c-460a-9cc7-47bdc031d841",
                "KeyValue": None,
                "KeyProperty": None,
                "DisplayName": "Sygeplejerske (Sygepleje (V) [SYGEPLEJE (V)]) ID:(00001234) ;",
            },
        ],
        # Addresses
        "EMAIL": "arthas@egepost.dk",
        "PHONE": "22334455",
        "CELLPHONE": "55443322",
        # IT Users
        "OBJECTGUID": "36-C9-80-88-A5-68-8A-47-BC-2C-2A-36-2C-AF-4E-7B",
        "C_ADUSERNAME": "LK1337",
    }


def test_parse_user(egedal_omada_user: dict) -> None:
    """Test parsing of a user."""
    omada_user = EgedalOmadaUser.parse_obj(egedal_omada_user)
    assert omada_user.is_manual is False
    assert omada_user.ad_guid == UUID("c22cc1c7-45e8-8349-854f-daef0b32b878")


def test_parse_manual_user(manual_egedal_omada_user: dict) -> None:
    """Test parsing of a manual user."""
    omada_user = ManualEgedalOmadaUser.parse_obj(manual_egedal_omada_user)
    assert omada_user.is_manual is True
    assert omada_user.employments[0].job_title == "Prince"
    assert omada_user.employments[0].org_unit == "Lordaeron"
    assert omada_user.employments[0].employment_number == "1337"
    assert omada_user.employments[1].job_title == "Sygeplejerske"
    assert omada_user.employments[1].org_unit == "Sygepleje (V)"
    assert omada_user.employments[1].employment_number == "1234"


@pytest.mark.parametrize(
    "display_name,expected",
    [
        (
            "Administrativ medarbejder (Ølstykke Bibliotek [ØLSTYKKE BIBLIOTEK]) ID:(1234) ;",
            {
                "employment_number": "1234",
                "job_title": "Administrativ medarbejder",
                "org_unit": "Ølstykke Bibliotek",
            },
        ),
        (
            "Afdelingsleder (Boesagerskolen, 6+9 årgang [BOESAGERSKOLEN, 6+9 ÅRGANG]) ID:(1234) ;",
            {
                "employment_number": "1234",
                "job_title": "Afdelingsleder",
                "org_unit": "Boesagerskolen, 6+9 årgang",
            },
        ),
        (
            "Bibliotekar (Smørum Bibliotek [SMØRUM BIBLIOTEK]) ID:(1234) ;",
            {
                "employment_number": "1234",
                "job_title": "Bibliotekar",
                "org_unit": "Smørum Bibliotek",
            },
        ),
        (
            "CAS - Robot (Regnskab [REGNSKAB]) ID:(1234) ;",
            {
                "employment_number": "1234",
                "job_title": "CAS - Robot",
                "org_unit": "Regnskab",
            },
        ),
        (
            "Centerchef (By, kultur og fritid [BY, KULTUR OG FRITID]) ID:(1234) ;",
            {
                "employment_number": "1234",
                "job_title": "Centerchef",
                "org_unit": "By, kultur og fritid",
            },
        ),
        (
            "Eftervederlag (Byråd [BYRÅD]) ID:(1234) ;",
            {
                "employment_number": "1234",
                "job_title": "Eftervederlag",
                "org_unit": "Byråd",
            },
        ),
        (
            "Ergoterapeut (Dambo (V) [DAMBO (V)]) ID:(1234) ;",
            {
                "employment_number": "1234",
                "job_title": "Ergoterapeut",
                "org_unit": "Dambo (V)",
            },
        ),
        (
            "Ergoterapeut (Team Handicap §85 [TEAM HANDICAP §85]) ID:(1234) ;",
            {
                "employment_number": "1234",
                "job_title": "Ergoterapeut",
                "org_unit": "Team Handicap §85",
            },
        ),
        (
            "Ergoterapeut (Træning- & Hjælpemiddel [TRÆNING- & HJÆLPEMIDDEL]) ID:(1234) ;",
            {
                "employment_number": "1234",
                "job_title": "Ergoterapeut",
                "org_unit": "Træning- & Hjælpemiddel",
            },
        ),
        (
            "Klubassistent u/udd (Byggelegeplads Stengården [BYGGELEGEPLADS STENGÅRDEN]) ID:(1234) ;",
            {
                "employment_number": "1234",
                "job_title": "Klubassistent u/udd",
                "org_unit": "Byggelegeplads Stengården",
            },
        ),
        (
            "Lærer m/særlige kval. (Balsmoseskolen, 3-5 årgang [BALSMOSESKOLEN, 3-5 ÅRGANG]) ID:(1234) ;",
            {
                "employment_number": "1234",
                "job_title": "Lærer m/særlige kval.",
                "org_unit": "Balsmoseskolen, 3-5 årgang",
            },
        ),
        (
            "Mangler JobRole (Afdeling Børn (V) [AFDELING BØRN (V)]) ID:(1234) ;",
            {
                "employment_number": "1234",
                "job_title": "Mangler JobRole",
                "org_unit": "Afdeling Børn (V)",
            },
        ),
        (
            "Social- og sundhedsassistent (Afløsere (V) [AFLØSERE (V)]) ID:(1234) ;",
            {
                "employment_number": "1234",
                "job_title": "Social- og sundhedsassistent",
                "org_unit": "Afløsere (V)",
            },
        ),
        (
            "Uuddannet medarbejder (Etage 1 (V) [ETAGE 1 (V)]) ID:(1234) ;",
            {
                "employment_number": "1234",
                "job_title": "Uuddannet medarbejder",
                "org_unit": "Etage 1 (V)",
            },
        ),
    ],
)
def test_parse_employment(display_name: str, expected: dict) -> None:
    obj = {
        "DisplayName": display_name,
    }
    employment = EgedalOmadaEmployment.parse_obj(obj)
    assert employment.dict() == expected