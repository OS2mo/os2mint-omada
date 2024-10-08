# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import structlog
from fastapi import Depends
from fastramqpi.ramqp import Router
from fastramqpi.ramqp.depends import rate_limit
from fastramqpi.ramqp.mo import MORouter
from fastramqpi.ramqp.mo import PayloadType

from os2mint_omada.omada.event_generator import Event

from ... import depends
from ...depends import CurrentOmadaUser
from .address import sync_addresses
from .employee import sync_employee
from .engagement import sync_engagements
from .it_user import sync_it_users
from .models import FrederikshavnOmadaUser

logger = structlog.stdlib.get_logger()
mo_router = MORouter()
omada_router = Router()


#######################################################################################
# Omada
#######################################################################################
@omada_router.register(Event.WILDCARD, dependencies=[Depends(rate_limit())])
async def sync_omada_employee(
    current_omada_user: CurrentOmadaUser,
    mo: depends.MO,
) -> None:
    # TODO: Dependency-inject user instead
    omada_user = FrederikshavnOmadaUser.parse_obj(current_omada_user)

    await sync_employee(
        omada_user=omada_user,
        mo=mo,
    )


@omada_router.register(Event.WILDCARD, dependencies=[Depends(rate_limit())])
async def sync_omada_engagements(
    current_omada_user: CurrentOmadaUser,
    mo: depends.MO,
    omada_api: depends.OmadaAPI,
) -> None:
    # TODO: Dependency-inject user instead
    omada_user = FrederikshavnOmadaUser.parse_obj(current_omada_user)

    # Find employee in MO
    employee_uuid = await mo.get_employee_uuid_from_cpr(omada_user.cpr_number)
    if employee_uuid is None:
        logger.info("No employee in MO: skipping engagements synchronisation")
        return

    await sync_engagements(
        employee_uuid=employee_uuid,
        mo=mo,
        omada_api=omada_api,
    )


@omada_router.register(Event.WILDCARD, dependencies=[Depends(rate_limit())])
async def sync_omada_addresses(
    current_omada_user: CurrentOmadaUser,
    mo: depends.MO,
    omada_api: depends.OmadaAPI,
) -> None:
    # TODO: Dependency-inject user instead
    omada_user = FrederikshavnOmadaUser.parse_obj(current_omada_user)

    # Find employee in MO
    employee_uuid = await mo.get_employee_uuid_from_cpr(omada_user.cpr_number)
    if employee_uuid is None:
        logger.info("No employee in MO: skipping addresses synchronisation")
        return

    await sync_addresses(
        employee_uuid=employee_uuid,
        mo=mo,
        omada_api=omada_api,
    )


@omada_router.register(Event.WILDCARD, dependencies=[Depends(rate_limit())])
async def sync_omada_it_users(
    current_omada_user: CurrentOmadaUser,
    mo: depends.MO,
    omada_api: depends.OmadaAPI,
) -> None:
    # TODO: Dependency-inject user instead
    omada_user = FrederikshavnOmadaUser.parse_obj(current_omada_user)

    # Find employee in MO
    employee_uuid = await mo.get_employee_uuid_from_cpr(omada_user.cpr_number)
    if employee_uuid is None:
        logger.info("No employee in MO: skipping IT user synchronisation")
        return

    await sync_it_users(
        employee_uuid=employee_uuid,
        mo=mo,
        omada_api=omada_api,
    )


#######################################################################################
# MO
#######################################################################################
# TODO: MO ITUsers and Addresses are not watched since the Omada integration is
#  authoritative for these objects, so we do not expect them to be modified. This
#  invariant should be enforced by RBAC.


@mo_router.register("employee.employee.*", dependencies=[Depends(rate_limit())])
async def sync_mo_engagements(
    payload: PayloadType,
    mo: depends.MO,
    omada_api: depends.OmadaAPI,
) -> None:
    employee_uuid = payload.uuid
    await sync_engagements(
        employee_uuid=employee_uuid,
        mo=mo,
        omada_api=omada_api,
    )


@mo_router.register("employee.engagement.*", dependencies=[Depends(rate_limit())])
async def sync_mo_addresses(
    payload: PayloadType,
    mo: depends.MO,
    omada_api: depends.OmadaAPI,
) -> None:
    employee_uuid = payload.uuid
    await sync_addresses(
        employee_uuid=employee_uuid,
        mo=mo,
        omada_api=omada_api,
    )


@mo_router.register("employee.engagement.*", dependencies=[Depends(rate_limit())])
async def sync_mo_it_users(
    payload: PayloadType,
    mo: depends.MO,
    omada_api: depends.OmadaAPI,
) -> None:
    employee_uuid = payload.uuid
    await sync_it_users(
        employee_uuid=employee_uuid,
        mo=mo,
        omada_api=omada_api,
    )
