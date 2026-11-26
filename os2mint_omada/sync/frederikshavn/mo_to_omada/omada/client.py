# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from contextlib import asynccontextmanager
from typing import Any
from typing import AsyncIterator

import structlog
from fastramqpi.raclients.auth import AuthenticatedAsyncHTTPXClient
from httpx import AsyncClient
from httpx import Response
from pydantic import AnyHttpUrl
from pydantic import parse_obj_as

logger = structlog.stdlib.get_logger()


class OmadaClient:
    ORG_UNIT_PATH = "/OData/DataObjects/OrgUnit"

    def __init__(self, client: AsyncClient) -> None:
        """Client for the Omada OData API.

        Use `create_omada_client` to get an instance with an authenticated
        HTTP client.

        Args:
            client: HTTPX client with the base URL of the Omada instance.
        """
        self.client = client

    async def get_org_units(
        self,
        odata_filter: str | None = None,
        select: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """List organisational units (GET /OData/DataObjects/OrgUnit).

        Args:
            odata_filter: Optional OData filter, e.g. "OUID eq 'abc'".
            select: Optional list of fields to return, e.g. ["OUID", "NAME"].

        Returns: List of raw Omada org units (dicts).
        """
        params = {}
        if odata_filter is not None:
            params["$filter"] = odata_filter
        if select is not None:
            params["$select"] = ",".join(select)

        logger.info("Getting Omada org units", params=params)

        response = await self.client.get(self.ORG_UNIT_PATH, params=params)
        response.raise_for_status()

        org_units: list[dict[str, Any]] = response.json()["value"]

        logger.debug("Retrieved Omada org units", org_units=org_units)

        return org_units

    async def create_org_unit(
        self,
        org_unit: dict[str, Any],
        select: list[str] | None = None,
    ) -> dict[str, Any] | None:
        """Create an organisational unit (POST /OData/DataObjects/OrgUnit).

        Args:
            org_unit: Raw Omada org unit, e.g.
             {"OUID": "MY_OU", "NAME": "My OU", "OUTYPE": {"UId": "..."},
             "PARENTOU": {"KeyValue": "PARENT_OU"}}.
            select: Optional list of fields to return, e.g. ["id", "OUID"].

        Returns: The created raw Omada org unit, or None if Omada returned no body.
        """
        logger.info("Creating Omada org unit", org_unit=org_unit)

        response = await self.client.post(
            self.ORG_UNIT_PATH, json=org_unit, params=self._select_params(select)
        )
        response.raise_for_status()

        return self._json_or_none(response)

    async def update_org_unit(
        self,
        id: int,
        org_unit: dict[str, Any],
        select: list[str] | None = None,
    ) -> dict[str, Any] | None:
        """Update an organisational unit (PUT /OData/DataObjects/OrgUnit(id)).

        Args:
            id: Omada ID of the org unit (the "id" field, not "uid" or "OUID").
            org_unit: Raw Omada org unit fields to update, e.g. {"NAME": "My OU"}.
            select: Optional list of fields to return, e.g. ["id", "NAME"].

        Returns: The updated raw Omada org unit, or None if Omada returned no body.
        """
        logger.info("Updating Omada org unit", id=id, org_unit=org_unit)

        response = await self.client.put(
            self._org_unit_path(id), json=org_unit, params=self._select_params(select)
        )
        response.raise_for_status()

        return self._json_or_none(response)

    async def delete_org_unit(self, id: int) -> None:
        """Delete an organisational unit (DELETE /OData/DataObjects/OrgUnit(id)).

        Args:
            id: Omada ID of the org unit (the "id" field, not "uid" or "OUID").
        """
        logger.info("Deleting Omada org unit", id=id)

        response = await self.client.delete(self._org_unit_path(id))
        response.raise_for_status()

    def _org_unit_path(self, id: int) -> str:
        return f"{self.ORG_UNIT_PATH}({id})"

    @staticmethod
    def _select_params(select: list[str] | None) -> dict[str, str]:
        if select is None:
            return {}
        return {"$select": ",".join(select)}

    @staticmethod
    def _json_or_none(response: Response) -> dict[str, Any] | None:
        if not response.content:
            return None
        result: dict[str, Any] = response.json()
        return result


@asynccontextmanager
async def create_omada_client(
    base_url: str,
    token_url: str,
    scope: str,
    client_id: str,
    client_secret: str,
    timeout: float = 60,
) -> AsyncIterator[OmadaClient]:
    """Create an Omada client which authenticates using OpenID Connect.

    The token is fetched with grant_type=client_credentials (and refreshed
    when it expires) automatically and sent in an "Authorization: Bearer"
    header. The underlying HTTP client is closed when the context exits.

    Args:
        base_url: Base URL of the Omada instance, e.g.
         https://demo-dev.omada.cloud.
        token_url: OpenID Connect token endpoint.
        scope: Scope to request the token for, e.g.
         https://demo-dev.omada.cloud/.default.
        client_id: OpenID Connect client ID.
        client_secret: OpenID Connect client secret.
        timeout: HTTP timeout in seconds.

    Yields: Authenticated Omada client.
    """
    async with AuthenticatedAsyncHTTPXClient(
        base_url=base_url,
        token_endpoint=parse_obj_as(AnyHttpUrl, token_url),
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        timeout=timeout,
    ) as http_client:
        yield OmadaClient(http_client)
