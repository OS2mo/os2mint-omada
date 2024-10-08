# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import structlog
from fastapi import APIRouter
from fastapi import status

from os2mint_omada import depends
from os2mint_omada.omada.event_generator import Event
from os2mint_omada.omada.models import RawOmadaUser

router = APIRouter()
logger = structlog.stdlib.get_logger()


@router.post("/sync/omada", status_code=status.HTTP_204_NO_CONTENT)
async def sync_omada(
    omada_api: depends.OmadaAPI,
    omada_amqp_system: depends.OmadaAMQPSystem,
    omada_filter: str | None = None,
) -> None:
    """Force-synchronise Omada user(s) matching the given Omada filter."""
    logger.info("Synchronising Omada users", omada_filter=omada_filter)
    raw_omada_users = await omada_api.get_users(omada_filter)
    logger.info("Synchronising raw Omada users", omada_users=raw_omada_users)
    for raw_omada_user in raw_omada_users:
        await omada_amqp_system.publish_message(
            routing_key=Event.REFRESH,
            payload=raw_omada_user,
        )


@router.get("/get-users")
async def get_users(
    omada_api: depends.OmadaAPI, omada_filter: str | None = None
) -> list[RawOmadaUser]:
    """Get Omada user(s) matching the given Omada filter."""
    raw_omada_users = await omada_api.get_users(omada_filter)
    return raw_omada_users
