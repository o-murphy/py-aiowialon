# pylint: disable=missing-module-docstring,line-too-long,missing-class-docstring
from typing_extensions import TypedDict, Required, Any, Literal
from aiowialon.types.flags import TokenFlag

Incomplete = Any


# token/update
class TokenProps(TypedDict, total=False):
    h: str | None  # token name - 72 symbols (while update, delete)
    app: Required[str | None]
    at: Required[int]  # token activation time, UNIX-time: 0 - now
    dur: Required[
        int
    ]  # token duration after activation, seconds: max value = 8640000 (100 days) if 0 – duration is infinite
    fl: Required[TokenFlag]
    p: Any | list[Any] | None
    items: list[int] | None


class TokenUpdateParams(TypedDict, total=False):
    callMode: Required[Literal["creation", "editing", "deletion"]]
    userId: str | None  # subuser id (optional, for managing other user tokens)
    h: str | None  # token name - 72 symbols (while update, delete)
    app: Required[str | None]
    at: Required[int]  # token activation time, UNIX-time: 0 - now
    dur: Required[
        int
    ]  # token duration after activation, seconds: max value = 8640000 (100 days) if 0 – duration is infinite
    fl: Required[TokenFlag]
    p: Any | list[Any] | None
    items: list[int] | None
    deleteAll: (
        bool | None
    )  # actual for callMode:delete; values: 1 or true - delete all created tokens


class TokenUpdateResponse(TypedDict):
    h: str
    app: str
    at: int
    ct: int  # token creation time, UNIX-time
    dur: int
    fl: TokenFlag
    p: Any | list[Any]
    items: list[int]


# token/list
class TokenListParams(TypedDict):
    userId: Required[int]


class TokenListResponse(TypedDict):
    h: str
    app: str
    at: int
    ct: int  # token creation time, UNIX-time
    dur: int
    fl: TokenFlag
    ll: int
    ttl: int
    items: list[int]
    p: Any | list[Any]


# token/login


class TokenLoginParams(TypedDict, total=False):
    token: Required[str]
    operateAs: str | None
    fl: Required[Incomplete]


class TokenLoginUserCustomProps(TypedDict):  # Possibly incomplete
    dst: str
    language: str
    msakey: str
    pcal: str
    tz: str
    us_units: str
    # other there


class TokenLoginUser2FactorAuth(TypedDict):
    type: Incomplete  # 0 - none, 1 - email, 2 - SMS
    phone: str


class TokenLoginUser(TypedDict):
    nm: str
    cls: int
    id: int
    prp: TokenLoginUserCustomProps
    crt: int
    bact: int
    fl: Incomplete
    hm: str
    uacl: int
    mu: int
    ct: int
    ftp: Incomplete
    ld: int
    pfl: int
    ap: TokenLoginUser2FactorAuth
    mapps: Incomplete
    mappsmax: int


class TokenLoginClasses(TypedDict):
    avl_hw: int
    avl_resource: int
    avl_retranslator: int
    avl_unit: int
    avl_unit_group: int
    user: int
    avl_route: int


class TokenLoginResponse(TypedDict):
    eid: str
    gis_sid: str
    host: str
    hw_gw_ip: str
    au: str
    pi: int
    tm: int
    wsdk_version: str
    user: TokenLoginUser
    classes: TokenLoginClasses
    features: Incomplete
    token: str  # all token settings as escaped json
