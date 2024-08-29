# pylint: disable=missing-module-docstring,line-too-long,missing-class-docstring
from enum import IntEnum

from typing_extensions import TypedDict, Required, Optional, Any, List, Literal
from aiowialon.utils.compat import StrEnum

Incomplete = Any


# retranslator/update_units
class RetranslatorUnitProps(TypedDict, total=False):
    a: Required[str]
    i: Required[int]
    st: Optional[int]


class RetranslatorUpdateUnitsParams(TypedDict, total=False):
    itemId: Required[int]
    units: Required[List[RetranslatorUnitProps]]
    callMode: Optional[Literal['add', 'remove']]


class RetranslatorUpdateUnitsResponse(TypedDict):
    rtru: List[RetranslatorUnitProps]


# retranslator/update_operating
class RetranslatorUpdateOperatingParams(TypedDict, total=False):
    itemId: Required[int]
    operate: Required[bool]
    stopTime: Optional[int]
    timeFrom: Optional[int]  # interval beginning of history retranslation, UNIX - time (only for history)
    timeTo: Optional[int]  # interval end of history retranslation, UNIX - time (only for history)
    callMode: Optional[
        Literal['start', 'stop']]  # switch - start/stop retranslator, history - start/stop history retranslation


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
    WIALON = 'wialon'
    WIALON_IPS = 'wialon_ips'
    NIS = 'nis'
    GRANIT3 = 'granit3'
    NAVIGATOR = 'navigator'
    SKAUT = 'skaut'
    CYBER_GLX = 'cyber_glx'
    GLX = 'glx'
    VT300 = 'vt300'
    EGTS = 'egts'
    SOAP = 'soap'


class Check(IntEnum):
    NO = 0
    YES = 1


class RetranslatorConfig(TypedDict, total=False):
    protocol: Required[RetranslatorProtocol]
    server: Required[str]
    port: Optional[str]  # port (for all except NIS)
    v6type: Optional[Check]  # use protocol v.6 (only for Granit Navigator)
    auth: Optional[str]  # authorization (only for NIS and Wialon IPS)
    attach_sensors: Optional[bool]  # retranslate calculated sensor values (for для Wialon IPS & Wialon Retranslator)
    ssl: Optional[str]  # secure connection (for NIS)
    login: Required[str]
    password: Required[str]
    notauth: Optional[Check]  # disable autorization (only for EGTS)


class RetranslatorUpdateConfigParams(TypedDict):
    itemId: Required[int]
    config: Required[RetranslatorConfig]


class RetranslatorUpdateConfigResponse(TypedDict):
    rtrc: List[RetranslatorConfig]
