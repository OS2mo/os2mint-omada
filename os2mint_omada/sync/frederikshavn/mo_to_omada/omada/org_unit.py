# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from typing import Any
from uuid import UUID

from more_itertools import only

from os2mint_omada.sync.frederikshavn.mo_to_omada.models import MOOrgUnit
from os2mint_omada.sync.frederikshavn.mo_to_omada.models import OmadaOrgUnit
from os2mint_omada.sync.frederikshavn.mo_to_omada.omada.client import OmadaClient


def _omada_attributes(mo_org_unit: MOOrgUnit) -> dict[str, Any]:
    """Omada org unit attributes according to MO."""
    # TODO: OUTYPE ({"UId": ...}) is not synchronised, as there is no known
    # mapping from MO org unit types to Omada OU types yet.
    return {
        "OUID": mo_org_unit.user_key,
        "NAME": mo_org_unit.name,
        "PARENTOU": ({"UId": str(mo_org_unit.parent)} if mo_org_unit.parent else None),
        "C_DEPARTMENTTYPE": mo_org_unit.org_unit_type,
    }


async def get_org_unit(omada_client: OmadaClient, uid: UUID) -> OmadaOrgUnit | None:
    """
    Get an Omada org unit by its UId.

    Args:
        omada_client: the Omada client
        uid: UId of the Omada org unit

    Returns:
        The Omada org unit if it exists or None otherwise.
    """
    # GUIDs are unquoted in OData v4 filters
    org_units = await omada_client.get_org_units(odata_filter=f"UId eq {uid}")

    # UIds are unique, so this raises if Omada returns more than one
    org_unit = only(org_units)
    if org_unit is None:
        return None

    # Reference attributes are returned as objects, e.g.
    # {"Id": 1000, "UId": "...", "DisplayName": "...", "KeyValue": "..."}
    parent = org_unit.get("PARENTOU")

    return OmadaOrgUnit(
        id=org_unit["Id"],
        ouid=org_unit["OUID"],
        name=org_unit["NAME"],
        parent_uid=parent["UId"] if parent else None,
        ou_type_id=org_unit["OUTYPE"]["Id"],
        c_departmenttype=org_unit["C_DEPARTMENTTYPE"],
    )


async def create_org_unit(
    omada_client: OmadaClient, uuid: UUID, mo_org_unit: MOOrgUnit
) -> None:
    """
    Create an Omada org unit according to the MO org unit.

    Args:
        omada_client: the Omada client
        uuid: UUID of the MO org unit, used as UId of the Omada org unit
        mo_org_unit: the MO org unit
    """
    await omada_client.create_org_unit(
        {"UId": str(uuid), **_omada_attributes(mo_org_unit)}
    )


async def update_org_unit(
    omada_client: OmadaClient, mo_org_unit: MOOrgUnit, omada_org_unit: OmadaOrgUnit
) -> None:
    """
    Update the Omada org unit attributes according to the MO org unit.

    Args:
        omada_client: the Omada client
        mo_org_unit: the MO org unit
        omada_org_unit: the Omada org unit to update
    """
    await omada_client.update_org_unit(
        omada_org_unit.id, _omada_attributes(mo_org_unit)
    )


async def delete_org_unit(
    omada_client: OmadaClient, omada_org_unit: OmadaOrgUnit
) -> None:
    """
    Delete the Omada org unit.

    Args:
        omada_client: the Omada client
        omada_org_unit: the Omada org unit to delete
    """
    await omada_client.delete_org_unit(omada_org_unit.id)
