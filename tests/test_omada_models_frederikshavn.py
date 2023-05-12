# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import pytest

from os2mint_omada.sync.frederikshavn.models import FrederikshavnOmadaUser


@pytest.fixture
def frederikshavn_omada_user() -> dict:
    """Frederikshavn Omada user, as returned by the API."""
    return {
        "Id": 1277266,
        "UId": "347a7d7a-49d6-4e90-93c8-88f3a0a40548",
        "CreateTime": "2023-01-31T08:51:06.397+01:00",
        "ChangeTime": "2023-04-18T11:39:56.29+02:00",
        "DisplayName": "Vikarsen, Vikar [93FCD3BE-DE85-473F-B602-4991AB4B41DC]",
        "IDENTITYID": None,
        "FIRSTNAME": "Vikar",
        "LASTNAME": "Vikarsen",
        "EMAIL": "VIVI04@frederikshavn.dk",
        "JOBTITLE": None,
        "VALIDFROM": "2021-01-31T08:44:00+01:00",
        "VALIDTO": "2024-02-01T08:44:00+01:00",
        "OISID": 48,
        "INITIALPASSWORD": None,
        "ODWBUSIKEY": None,
        "RISKSCORE": None,
        "STATE_REGION": None,
        "BIRTHDAY": None,
        "ADDRESS2": None,
        "ADDRESS1": None,
        "CITY": None,
        "ZIPCODE": None,
        "EMAIL2": None,
        "IDENTSODXML": None,
        "IDENTSODRECALCSURV": None,
        "PWR_LOCKOUT": None,
        "ADLOGON": "VIVI04",
        "C_ADDN": None,
        "C_NOITUSER": False,
        "C_MOBILE": None,
        "C_TELEPHONENUMBER": None,
        "C_POSTALCODE": None,
        "C_STREETADDRESS": None,
        "C_ISONBOARDE": None,
        "C_POSITIONID": "00120589",
        "C_CPRNUMBER": "120390-0593",
        "C_EXTPERSONALEMAIL": None,
        "JOBTITLE_ID": None,
        "CELLPHONE": None,
        "C_ONBOARDING_MAIL_SENT": None,
        "C_DEPARTMENTTYPE": None,
        "C_JOBTITLE_ODATA": "Vikar Sygeplejerske",
        "C_IDENCATEGORY_ODATA": "Vikar",
        "C_ORGUNIT_ODATA": "Sæby Ældrecenter",
        "C_MANDISNAME_ODATA": "Mogens Kahr Nielsen",
        "C_IDENTITYSTATUS_ODATA": "Terminated",
        "C_DISPLAYNAME_ODATA": None,
        "OUID": None,
        "C_OUID_ODATA": "01012415",
        "OUREF": {"Id": 1007117, "UId": None, "KeyValue": None, "KeyProperty": None},
        "IDENTITYSTATUS": {"Id": 552, "UId": "51895789-83d1-45fa-a0bf-ddcd94902f0e"},
        "IDENTITYCATEGORY": {
            "Id": 1000245,
            "UId": "7e7b6153-539d-459a-b47b-2500ddb76543",
        },
        "IDENTITYTYPE": None,
        "IDENTITYOWNER": None,
        "PRIMARYCONTEXTTYPE": None,
        "TIMEZONE": None,
        "EXPLICITOWNER": [],
        "MANAGER": [
            {"Id": 1020834, "UId": None, "KeyValue": None, "KeyProperty": None}
        ],
        "GENDER": None,
        "COUNTRY": None,
        "CLT_TAGS": [],
        "EMPLOYMENTS": [],
        "RISKLEVEL": None,
        "SUBAREA": None,
        "BUILDING": None,
        "JOBTITLE_REF": {
            "Id": 1272062,
            "UId": None,
            "KeyValue": None,
            "KeyProperty": None,
        },
        "DIVISION": None,
        "BUSINESSUNIT": None,
        "COMPANY": None,
        "COSTCENTER": None,
        "LOCATION": None,
        "C_EXTERNALCOMPANYREF": None,
        "C_EXTERNALTYPEREF": None,
        "C_EXTERNALRISKLEVELREF": None,
    }


def test_parse_user(frederikshavn_omada_user: dict) -> None:
    """Test parsing of a user."""
    assert FrederikshavnOmadaUser.parse_obj(frederikshavn_omada_user)
