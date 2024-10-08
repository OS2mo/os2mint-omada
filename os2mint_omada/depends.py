# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from typing import Annotated

from fastapi import Depends
from fastramqpi.depends import from_user_context
from fastramqpi.ramqp import AMQPSystem
from fastramqpi.ramqp.depends import from_context
from fastramqpi.ramqp.depends import get_payload_as_type
from more_itertools import only
from pydantic import parse_obj_as

from os2mint_omada.autogenerated_graphql_client import GraphQLClient as _GraphQLClient
from os2mint_omada.mo import MO as _MO
from os2mint_omada.omada.api import OmadaAPI as _OmadaAPI
from os2mint_omada.omada.models import OmadaUser

GraphQLClient = Annotated[_GraphQLClient, Depends(from_context("graphql_client"))]

# Omada context
OmadaAMQPSystem = Annotated[AMQPSystem, Depends(from_user_context("omada_amqp_system"))]
OmadaAPI = Annotated[_OmadaAPI, Depends(from_user_context("omada_api"))]


async def current_omada_user(
    amqp_user: Annotated[OmadaUser, Depends(get_payload_as_type(OmadaUser))],
    omada_api: OmadaAPI,
) -> OmadaUser:
    """Return the latest state of an Omada user.

    The Omada user contained in the AMQP message might be stale, e.g. if it was created
    with an invalid CPR-number and then later corrected. To avoid failing to parse the
    invalid user forever, handlers should always use the latest data from the API. Note
    that the user might have been deleted from the Omada API view, in which case the
    data from the AMQP event payload is returned instead.
    """
    # NOTE: Old versions of Omada (i.e. the version our customers use) do not support filtering on UId, so we filter on Id instead.
    api_users_raw = await omada_api.get_users_by("Id", [amqp_user.id])
    if not api_users_raw:
        return amqp_user
    return parse_obj_as(OmadaUser, only(api_users_raw))


CurrentOmadaUser = Annotated[OmadaUser, Depends(current_omada_user)]


def get_mo(graphql_client: GraphQLClient) -> _MO:
    return _MO(graphql_client)


MO = Annotated[_MO, Depends(get_mo)]
