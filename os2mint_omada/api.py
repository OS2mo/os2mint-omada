# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import asyncio
from typing import Any

from fastapi import APIRouter

from os2mint_omada import mo
from os2mint_omada import omada
from os2mint_omada import sync
from os2mint_omada.clients import model_client
from os2mint_omada.config import settings

router = APIRouter()


@router.post("/import/it-users")
async def import_it_users() -> dict[str, Any]:
    """
    Import Omada IT users into MO.

    Returns: Dictionary of statistics.
    """
    # Get user information from MO and Omada
    root_org_uuid = await mo.get_root_org()
    it_system_uuid = await mo.get_it_system_uuid(
        organisation_uuid=root_org_uuid,
        user_key=settings.it_system_user_key,
    )
    address_classes = asyncio.create_task(mo.get_address_classes(root_org_uuid))
    mo_it_bindings = asyncio.create_task(mo.get_it_bindings(it_system_uuid))
    mo_user_addresses = asyncio.create_task(mo.get_user_addresses())
    mo_engagements = asyncio.create_task(mo.get_engagements())
    omada_it_users = asyncio.create_task(omada.get_it_users(settings.odata_url))

    # Synchronise updated objects to MO
    updated_objects = list(
        sync.get_updated_mo_objects(
            mo_it_bindings=await mo_it_bindings,
            omada_it_users=await omada_it_users,
            mo_user_addresses=await mo_user_addresses,
            mo_engagements=await mo_engagements,
            address_class_uuids=await address_classes,
            it_system_uuid=it_system_uuid,
        )
    )
    async with model_client.context():
        await model_client.load_mo_objs(updated_objects)

    return dict(
        num_updated_objects=len(updated_objects),
    )
