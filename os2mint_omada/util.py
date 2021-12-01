# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from datetime import date
from datetime import datetime
from typing import Optional
from typing import TypeVar

from ramodels.mo._shared import Validity
from ramodels.mo.details import Address
from ramodels.mo.details import ITSystemBinding

MOBaseWithValidity = TypeVar("MOBaseWithValidity", Address, ITSystemBinding)


def midnight() -> date:
    return datetime.utcnow().date()


def as_terminated(
    model: MOBaseWithValidity, from_date: Optional[date] = None
) -> MOBaseWithValidity:
    return model.parse_obj(  # pydantic doesn't validate on .copy()
        model.copy(
            update=dict(
                validity=Validity(
                    from_date=model.validity.from_date,
                    to_date=from_date if from_date is not None else midnight(),
                ),
            )
        )
    )
