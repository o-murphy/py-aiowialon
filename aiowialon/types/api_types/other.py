# pylint: disable=missing-module-docstring,line-too-long,missing-class-docstring
from typing import TypedDict, Any
from aiowialon.utils.compat import StrEnum


class AvlEventType(StrEnum):
    """AVL event types"""

    MESSAGE = "m"
    UPDATE = "u"
    DELETE = "d"


class AvlEventInstance(TypedDict):
    i: int
    t: AvlEventType
    d: dict[str, Any]


class AvlEventResponse(TypedDict):
    tm: int
    events: list[AvlEventInstance]
