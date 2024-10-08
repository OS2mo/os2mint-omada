# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from __future__ import annotations

from collections import defaultdict

import structlog
from fastramqpi.ramqp.depends import handle_exclusively_decorator

from os2mint_omada.mo import MO

from ...autogenerated_graphql_client import EmployeeCreateInput
from ..models import ComparableEmployee
from ..models import Employee
from .models import ManualSilkeborgOmadaUser

logger = structlog.stdlib.get_logger()


@handle_exclusively_decorator(key=lambda omada_user, *_, **__: omada_user.cpr_number)
async def sync_manual_employee(
    omada_user: ManualSilkeborgOmadaUser,
    mo: MO,
) -> None:
    logger.info("Synchronising employee", omada_user=omada_user)

    # Find employee in MO
    employee_uuid = await mo.get_employee_uuid_from_cpr(omada_user.cpr_number)

    if employee_uuid is not None:
        logger.info("Not modifying existing employee", employee_uuid=employee_uuid)
        return

    employee_states: set[Employee] = set()
    if employee_uuid is not None:
        employee_states = await mo.get_employee_states(uuid=employee_uuid)

    # Existing employee states in MO
    existing: defaultdict[ComparableEmployee, set[Employee]] = defaultdict(set)
    for mo_employee_state in employee_states:
        comparable_employee = ComparableEmployee(**mo_employee_state.dict())
        existing[comparable_employee].add(mo_employee_state)

    # Desired employee states from Omada (only one)
    desired = {
        ComparableEmployee(
            given_name=omada_user.first_name,
            surname=omada_user.last_name,
            cpr_number=omada_user.cpr_number,
        )
    }

    # Delete excess existing
    # TODO: Implement when supported by MO

    # Create missing desired
    missing_comparable = desired - existing.keys()
    missing_mo = [Employee(**employee.dict()) for employee in missing_comparable]
    if missing_mo:
        logger.info("Creating missing Employee states", employees=missing_mo)
        for missing in missing_mo:
            # GraphQL employee_create actually updates if the employee already exists.
            # This is better than an explicit update, since that would require us to
            # calculate the validity manually based on CPR.
            await mo.graphql_client.create_employee(
                EmployeeCreateInput(
                    uuid=employee_uuid,
                    given_name=missing.given_name,
                    surname=missing.surname,
                    cpr_number=missing.cpr_number,
                    nickname_given_name=missing.nickname_given_name,
                    nickname_surname=missing.nickname_surname,
                )
            )
