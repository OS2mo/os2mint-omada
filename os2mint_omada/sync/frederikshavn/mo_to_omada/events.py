# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from uuid import UUID

import structlog
from fastapi import APIRouter
from fastramqpi.events import Event

from os2mint_omada import depends
from os2mint_omada.sync.frederikshavn.mo_to_omada.sync.org_unit import sync_ou

router = APIRouter()
logger = structlog.stdlib.get_logger()


@router.post("/events/mo/org-unit")
async def sync_org_unit(
    event: Event[UUID],
    graphql_client: depends.GraphQLClient,
    omada_client: depends.OmadaClient,
) -> None:
    """
    Handle org unit events from MO's GraphQL event system by synchronising the
    org unit to Omada.
    """
    logger.info("Received MO org unit event", org_unit_uuid=event.subject)
    await sync_ou(graphql_client, omada_client, event.subject)
