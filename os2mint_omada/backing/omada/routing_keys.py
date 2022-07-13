# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from enum import Enum

from pydantic import BaseModel


class Event(str, Enum):
    """Omada AMQP event type."""

    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class Type(str, Enum):
    """Omada AMQP payload type."""

    RAW = "raw"
    PARSED = "parsed"


class RoutingKey(BaseModel):
    """Omada AMQP routing key."""

    event: Event
    type: Type

    def __str__(self) -> str:
        return f"omada.user.{self.event}.{self.type}"


class RawRoutingKey(RoutingKey):
    """Omada AMQP routing key for raw payloads."""

    type = Type.RAW


class IdentityCategory(str, Enum):
    """TODO"""

    NORMAL = "normal"
    MANUAL = "manual"


class ParsedRoutingKey(RoutingKey):
    """Omada AMQP routing key for parsed payloads."""

    type = Type.PARSED
    identity_category: IdentityCategory

    def __str__(self) -> str:
        return f"{super().__str__()}.{self.identity_category}"
