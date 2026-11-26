# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from uuid import UUID

from pydantic import BaseModel
from pydantic import PositiveInt


class MOOrgUnit(BaseModel):
    user_key: str
    name: str
    parent: UUID | None
    org_unit_type: str


class OmadaOrgUnit(BaseModel):
    id: int
    ouid: str
    name: str
    parent_uid: UUID | None
    ou_type_id: PositiveInt
    c_departmenttype: str
