# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import pytest

from os2mint_omada.sync.silkeborg.models import ManualSilkeborgOmadaUser
from os2mint_omada.sync.silkeborg.models import SilkeborgOmadaUser


@pytest.fixture
def silkeborg_omada_user() -> dict:
    """Silkeborg Omada user, as returned by the API."""
    return {
        "Id": 1041073,
        "UId": "e9802c93-ce17-41e6-b425-5ed3c9e41b4f",
        "CreateTime": "2018-11-05T14:48:14.95+01:00",
        "ChangeTime": "2022-06-14T13:59:41.11+02:00",
        "DisplayName": "Anders W. Lemming [DRV2639]",
        "IDENTITYID": None,
        "FIRSTNAME": None,
        "LASTNAME": "Lemming",
        "EMAIL": "AndersW.Lemming@silkeborg.dk",
        "JOBTITLE": "",
        "VALIDFROM": "2016-06-15T00:00:00+02:00",
        "VALIDTO": "2022-12-03T00:00:00+01:00",
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
        "C_APPOINTCODE": None,
        "C_JOBPOSTIDENT": None,
        "C_DEP_DEACT_DATE": None,
        "C_DEP_ACT_DATE": None,
        "C_LOKALENAVN": None,
        "C_DIREKTE_TLF": "",
        "C_GOLOGIN": None,
        "C_O365": None,
        "C_INST_PHONE": "",
        "C_PRIV_MOBILNR": None,
        "C_PRIV_PHONE": None,
        "C_PRIV_COUNTRY": None,
        "C_PRIV_ZIP": None,
        "C_PRIV_CITY": None,
        "C_PRIV_ADDRESS": None,
        "C_PRIV_EMAIL": None,
        "C_INST_NAME": None,
        "C_FAX": None,
        "C_SEN_DATE": None,
        "C_SALARY_SCALE": None,
        "C_SALARY_CLASS": None,
        "C_SALARY_AGREE": None,
        "C_PENSIONCODE": None,
        "C_SALARYRATE": None,
        "C_OCCUP_RATE": None,
        "C_EMP_DEACT_DATE": None,
        "C_EMP_ACT_DATE": None,
        "C_EMP_STAT_CODE": None,
        "C_EAN": None,
        "C_KOMMENTAR": None,
        "C_FILSERVER": None,
        "C_MIDDLENAME": None,
        "C_TJENESTENR": "bbb",
        "C_CPRNR": "1907792583",
        "C_VALIDFROM_SD": None,
        "C_VALIDTO_SD": None,
        "CELLPHONE": "12345678",
        "C_SLETTET_SD": None,
        "C_PHONE_WEB": None,
        "C_SALARY_IND": None,
        "C_DATA_WEB": None,
        "C_FULLTIME": None,
        "C_PREPAY": None,
        "C_ITBRUGER_TID": None,
        "C_ITBRUGER": None,
        "C_FULLNAME": None,
        "C_FIRMA": None,
        "C_TITEL_SD": None,
        "C_DESCRIPTION": None,
        "C_SLETTEMAIL": None,
        "C_ITBRUGER_SLET": None,
        "C_LEDER_ANDR": None,
        "OISID": None,
        "C_EKSTRAFELT": None,
        "C_FORNAVNE": "Anders W.",
        "C_ANS_PROC_START": None,
        "C_SIMS_USER_CODE": None,
        "C_SIMS_CARD_CODE": None,
        "C_SIMS_PIN_CODE": None,
        "C_SIMS_INFO": None,
        "C_OBJECTGUID_I_AD": "b71dccac-6611-4bf7-bb09-77c0bf510210",
        "C_SIPADRESSE": None,
        "C_LOGIN": "DRV2639",
        "C_SYNLIG_I_OS2MO": True,
        "C_OPRETTES_I_OS2MO": None,
        "C_ORGANISATIONSKODE": "5a23d722-1be4-4f00-a200-000001500001",
        "C_INSTITUTIONSKODE": None,
        "OUREF": None,
        "IDENTITYSTATUS": None,
        "IDENTITYCATEGORY": {"Id": 564, "UId": "270a1807-95ca-40b4-9ce5-475d8961f31b"},
        "IDENTITYTYPE": None,
        "IDENTITYOWNER": None,
        "PRIMARYCONTEXTTYPE": None,
        "TIMEZONE": None,
        "EXPLICITOWNER": [],
        "MANAGER": [],
        "GENDER": None,
        "COUNTRY": None,
        "CLT_TAGS": [],
        "C_SEKTION": None,
        "C_TEKLEJE": None,
        "C_AFDELING": None,
        "C_BRUGERTYPE": None,
        "C_AFDELING_SIKO": None,
        "C_LEDER": None,
        "C_BEST_IDENT": None,
        "C_SIKOREF": None,
        "EMPLOYMENTS": [],
        "RISKLEVEL": None,
        "C_O365_SETP": None,
        "C_SEKTION_I_SIKO": None,
        "SUBAREA": None,
        "BUILDING": None,
        "JOBTITLE_REF": None,
        "DIVISION": None,
        "BUSINESSUNIT": None,
        "COMPANY": None,
        "COSTCENTER": None,
        "LOCATION": None,
        "C_AFDELING_TMP": None,
        "C_OPRETPROC": None,
        "C_OPRETTER": None,
    }


@pytest.fixture
def manual_silkeborg_omada_user() -> dict:
    """Manual Silkeborg Omada user, as returned by the API."""
    return {
        "Id": 1041094,
        "UId": "38e4a0f1-1290-40e3-ad83-896abd1d3e50",
        "CreateTime": "2018-11-05T14:48:18.693+01:00",
        "ChangeTime": "2022-05-10T09:35:55.35+02:00",
        "DisplayName": "Ida Jensen [DRV1216]",
        "IDENTITYID": None,
        "FIRSTNAME": None,
        "LASTNAME": "Hansen",
        "EMAIL": "Mia.Hansen@silkeborg.dk",
        "JOBTITLE": "Revisor",
        "VALIDFROM": "2012-08-27T00:00:00+02:00",
        "VALIDTO": "2022-12-01T01:00:00+01:00",
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
        "C_APPOINTCODE": None,
        "C_JOBPOSTIDENT": None,
        "C_DEP_DEACT_DATE": None,
        "C_DEP_ACT_DATE": None,
        "C_LOKALENAVN": None,
        "C_DIREKTE_TLF": "",
        "C_GOLOGIN": None,
        "C_O365": None,
        "C_INST_PHONE": "666666",
        "C_PRIV_MOBILNR": None,
        "C_PRIV_PHONE": None,
        "C_PRIV_COUNTRY": None,
        "C_PRIV_ZIP": None,
        "C_PRIV_CITY": None,
        "C_PRIV_ADDRESS": None,
        "C_PRIV_EMAIL": None,
        "C_INST_NAME": None,
        "C_FAX": None,
        "C_SEN_DATE": None,
        "C_SALARY_SCALE": None,
        "C_SALARY_CLASS": None,
        "C_SALARY_AGREE": None,
        "C_PENSIONCODE": None,
        "C_SALARYRATE": None,
        "C_OCCUP_RATE": None,
        "C_EMP_DEACT_DATE": None,
        "C_EMP_ACT_DATE": None,
        "C_EMP_STAT_CODE": None,
        "C_EAN": None,
        "C_KOMMENTAR": None,
        "C_FILSERVER": None,
        "C_MIDDLENAME": None,
        "C_TJENESTENR": "v1216",
        "C_CPRNR": "1709933104",
        "C_VALIDFROM_SD": None,
        "C_VALIDTO_SD": None,
        "CELLPHONE": "",
        "C_SLETTET_SD": None,
        "C_PHONE_WEB": None,
        "C_SALARY_IND": None,
        "C_DATA_WEB": None,
        "C_FULLTIME": None,
        "C_PREPAY": None,
        "C_ITBRUGER_TID": None,
        "C_ITBRUGER": None,
        "C_FULLNAME": None,
        "C_FIRMA": None,
        "C_TITEL_SD": None,
        "C_DESCRIPTION": None,
        "C_SLETTEMAIL": None,
        "C_ITBRUGER_SLET": None,
        "C_LEDER_ANDR": None,
        "OISID": None,
        "C_EKSTRAFELT": None,
        "C_FORNAVNE": "Mia",
        "C_ANS_PROC_START": None,
        "C_SIMS_USER_CODE": None,
        "C_SIMS_CARD_CODE": None,
        "C_SIMS_PIN_CODE": None,
        "C_SIMS_INFO": None,
        "C_OBJECTGUID_I_AD": "74dea272-d90b-47c7-8d99-c8efa372fa03",
        "C_SIPADRESSE": None,
        "C_LOGIN": "DRV1216",
        "C_SYNLIG_I_OS2MO": False,
        "C_OPRETTES_I_OS2MO": None,
        "C_ORGANISATIONSKODE": "f06ee470-9f17-566f-acbe-e938112d46d9",
        "C_INSTITUTIONSKODE": None,
        "OUREF": None,
        "IDENTITYSTATUS": None,
        "IDENTITYCATEGORY": {"Id": 561, "UId": "270a1807-95ca-40b4-9ce5-475d8961f31b"},
        "IDENTITYTYPE": None,
        "IDENTITYOWNER": None,
        "PRIMARYCONTEXTTYPE": None,
        "TIMEZONE": None,
        "EXPLICITOWNER": [],
        "MANAGER": [],
        "GENDER": None,
        "COUNTRY": None,
        "CLT_TAGS": [],
        "C_SEKTION": None,
        "C_TEKLEJE": None,
        "C_AFDELING": None,
        "C_BRUGERTYPE": None,
        "C_AFDELING_SIKO": None,
        "C_LEDER": None,
        "C_BEST_IDENT": None,
        "C_SIKOREF": None,
        "EMPLOYMENTS": [],
        "RISKLEVEL": None,
        "C_O365_SETP": None,
        "C_SEKTION_I_SIKO": None,
        "SUBAREA": None,
        "BUILDING": None,
        "JOBTITLE_REF": None,
        "DIVISION": None,
        "BUSINESSUNIT": None,
        "COMPANY": None,
        "COSTCENTER": None,
        "LOCATION": None,
        "C_AFDELING_TMP": None,
        "C_OPRETPROC": None,
        "C_OPRETTER": None,
    }


def test_parse_user(silkeborg_omada_user: dict) -> None:
    """Test parsing of a user."""
    omada_user = SilkeborgOmadaUser.parse_obj(silkeborg_omada_user)
    assert omada_user.is_manual is False


def test_parse_manual_user(manual_silkeborg_omada_user: dict) -> None:
    """Test parsing of a manual user."""
    omada_user = ManualSilkeborgOmadaUser.parse_obj(manual_silkeborg_omada_user)
    assert omada_user.is_manual is True
