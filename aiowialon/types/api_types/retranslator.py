# pylint: disable=missing-module-docstring,line-too-long,missing-class-docstring
from enum import IntEnum
from typing import Literal

from typing_extensions import Any, Required, TypedDict

from aiowialon.utils.compat import StrEnum

Incomplete = Any


# retranslator/update_units
class RetranslatorUnitProps(TypedDict, total=False):
    a: Required[str]
    i: Required[int]
    st: int | None


class RetranslatorUpdateUnitsParams(TypedDict, total=False):
    itemId: Required[int]
    units: Required[list[RetranslatorUnitProps]]
    callMode: Literal["add", "remove"] | None


class RetranslatorUpdateUnitsResponse(TypedDict):
    rtru: list[RetranslatorUnitProps]


# retranslator/update_operating
class RetranslatorUpdateOperatingParams(TypedDict, total=False):
    itemId: Required[int]
    operate: Required[bool]
    stopTime: int | None
    timeFrom: (
        int | None
    )  # interval beginning of history retranslation, UNIX - time (only for history)
    timeTo: (
        int | None
    )  # interval end of history retranslation, UNIX - time (only for history)
    callMode: (
        Literal["start", "stop"] | None
    )  # switch - start/stop retranslator, history - start/stop history retranslation


class RetranslatorUpdateOperatingResponse(TypedDict, total=False):
    rtro: int
    rtrst: int


# retranslator/get_stats
class RetranslatorGetStatsParams(TypedDict):
    itemId: Required[int]


class RetranslatorGetStatsResponse(TypedDict):
    au: int
    ru: int
    hf: int
    ht: int
    hc: int
    hms: int
    hp: int


# retranslator/update_config
class RetranslatorProtocol(StrEnum):
    WIALON = "wialon"
    WIALON_IPS = "wialon_ips"
    NIS = "nis"
    GRANIT3 = "granit3"
    NAVIGATOR = "navigator"
    SKAUT = "skaut"
    CYBER_GLX = "cyber_glx"
    GLX = "glx"
    VT300 = "vt300"
    EGTS = "egts"
    SOAP = "soap"


class Check(IntEnum):
    NO = 0
    YES = 1


class RetranslatorConfig(TypedDict, total=False):
    protocol: Required[RetranslatorProtocol]
    server: Required[str]
    port: str | None  # port (for all except NIS)
    v6type: Check | None  # use protocol v.6 (only for Granit Navigator)
    auth: str | None  # authorization (only for NIS and Wialon IPS)
    attach_sensors: (
        bool | None
    )  # retranslate calculated sensor values (for для Wialon IPS & Wialon Retranslator)
    ssl: str | None  # secure connection (for NIS)
    login: Required[str]
    password: Required[str]
    notauth: Check | None  # disable autorization (only for EGTS)


class RetranslatorUpdateConfigParams(TypedDict):
    itemId: Required[int]
    config: Required[RetranslatorConfig]


class RetranslatorUpdateConfigResponse(TypedDict):
    rtrc: list[RetranslatorConfig]
