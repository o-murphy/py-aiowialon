# pylint: disable=missing-module-docstring,line-too-long,missing-class-docstring
from enum import IntEnum
from typing_extensions import (
    Any,
    TypedDict,
    Required,
    Literal,
)
from aiowialon.types import flags

Incomplete = Any


# core/logout
class CoreErrorCode(TypedDict, total=False):
    error: int
    reason: str | None


# core/get_account_data
class CoreGetAccountDataResponseType(IntEnum):
    MINIMAL = 1
    DETAILED = 2


class CoreGetAccountDataParams(TypedDict):
    type: Required[CoreGetAccountDataResponseType]


class AccountService(TypedDict, total=False):
    type: int
    usage: int
    maxUsage: int
    cost: str | None
    interval: int | None


class BillingPlan(TypedDict, total=False):
    flags: int
    blockBalance: int
    denyBalance: int
    minDaysCounter: int
    historyPeriod: int
    services: dict[str, AccountService]


class AccountSettings(TypedDict, total=False):
    balance: float
    plan: BillingPlan
    personal: BillingPlan
    combined: BillingPlan


class CoreGetAccountDataResponse(TypedDict, total=False):
    plan: str
    enabled: bool
    created: int
    flags: int
    balance: str
    daysCounter: int
    services: dict[str, AccountService] | None  # minimal only
    settings: AccountSettings | None  # detailed only
    siteAccess: dict[str, str] | None  # detailed only
    dealerRights: int
    subPlans: list[str]
    switchTime: int | None  # minimal only


# core/check_items_billing
class CoreChechItemsBillingParams(TypedDict):
    items: Required[list[int]]
    accessFlags: Required[int]
    serviceName: Required[str]


CoreChechItemsBillingResponse = list[int]


# core/check_accessors
class CoreCheckAccessorsAddDact(IntEnum):
    DONT_ADD = 0
    ADD = 1


class CoreCheckAccessorsParams(TypedDict):
    items: Required[list[int]]
    flags: Required[CoreCheckAccessorsAddDact]


class CoreCheckAccessorsAccessRights(TypedDict, total=False):
    acl: int
    dacl: int


CoreCheckAccessorsResponse = dict[str, dict[str, CoreCheckAccessorsAccessRights]]


# core/create_user
class CoreCreateUserParams(TypedDict):
    creatorId: Required[int]
    name: Required[str]
    password: Required[str]
    dataFlags: Required[int]


class CoreCreateUserResponse(TypedDict, total=False):
    item: Incomplete
    flags: int


# core/create_resource


class CoreCreateResourceParams(TypedDict):
    creatorId: Required[int]
    name: Required[str]
    dataFlags: Required[int]
    skipCreatorCheck: Required[bool]


class CoreCreateResourceResponse(TypedDict, total=False):
    item: Incomplete
    flags: int


# core/create_unit


class CoreCreateUnitParams(TypedDict):
    creatorId: Required[int]
    name: Required[str]
    dataFlags: Required[int]
    hwTypeId: Required[int]


class CoreCreateUnitResponse(TypedDict, total=False):
    item: Incomplete
    flags: int


# core/create_unit_group


class CoreCreateUnitGroupParams(TypedDict):
    creatorId: Required[int]
    name: Required[str]
    dataFlags: Required[int]


class CoreCreateUnitGroupResponse(TypedDict, total=False):
    item: Incomplete
    flags: int


# core/create_retranslator


class CoreCreateRetranslatorConfig(TypedDict, total=False):
    protocol: Required[str]
    server: Required[str]
    port: Required[int]  # for all except NIS
    auth: str | None
    ssl: bool | None  # for NIS
    debug: Required[bool]
    v6type: bool | None  # for GRANIT_NAVIGATOR only


class CoreCreateRetranslatorParams(TypedDict):
    creatorId: Required[int]
    name: Required[str]
    config: CoreCreateRetranslatorConfig
    dataFlags: Required[int]


class CoreCreateRetranslatorResponse(TypedDict, total=False):
    item: Incomplete
    flags: int


# core/create_unit_group


class CoreCreateRouteParams(TypedDict):
    creatorId: Required[int]
    name: Required[str]
    dataFlags: Required[int]


class CoreCreateRouteResponse(TypedDict, total=False):
    item: Incomplete
    flags: int


# core/search_item


class CoreSearchItemParams(TypedDict):
    id: Required[int]
    flags: Required[int]


class CoreSearchItemResponse(TypedDict, total=False):
    item: Incomplete
    flags: int


# core/search_items


class SearchItemsSpec(TypedDict, total=False):
    itemsType: Required[Incomplete]
    propName: Required[Incomplete]
    propValueMask: Required[str]
    sortType: Required[str]
    propType: str | None
    or_logic: bool | None


class CoreSearchItemsParams(TypedDict):
    spec: Required[SearchItemsSpec]
    force: Required[bool]
    flags: Required[int]
    from_: Required[int]
    to: Required[int]


class CoreSearchItemsResponse(TypedDict):
    searchSpec: SearchItemsSpec
    dataFlags: int
    totalItemsCount: int
    indexFrom: int
    indexTo: int
    items: list[Incomplete]


# core/update_data_flags
class CoreUpdateDataFlagsSpec(TypedDict, total=False):
    type: Required[Incomplete]
    data: Required[str | int | list[int]]
    flags: Required[flags.UnitsDataFlag]
    mode: Required[Incomplete]
    max_items: int | None


class CoreUpdateDataFlagsParams(TypedDict):
    spec: Required[list[CoreUpdateDataFlagsSpec]]


class CoreUpdateDataFlagsResponse(TypedDict):
    i: int
    d: dict[str, Incomplete]
    f: int


# core/get_hw_types

HwCategory = Literal["auto", "tracker", "mobile", "soft"]
HwFeature = Literal["wifi_pos"]

CoreGetHwTypesFilterType = Literal["name", "id", "type", "feature"]
CoreGetHwTypesFilter = str | int | list[int] | HwCategory | HwFeature


class CoreGetHwTypesParams(TypedDict):
    filterType: Required[CoreGetHwTypesFilterType]
    filterValue: Required[CoreGetHwTypesFilter]
    includeType: Required[int | bool]
    ignoreRename: Required[int | bool]


class CoreHwType(TypedDict, total=False):
    id: int
    uid2: int
    name: str
    hw_category: HwCategory | None
    tp: int
    up: int


CoreGetHwTypesResponse = list[CoreHwType]


# core/get_hw_cmds


class CoreGetHwCommandsParams(TypedDict, total=False):
    deviceTypeId: Required[int]
    unitId: int | None
    template: Required[bool]
    lang: Incomplete | None


CoreGetHwCommandsList = dict[Incomplete, list[Incomplete]]


class HwCommandsTemplate(TypedDict):
    icon: str
    props: list[Incomplete]


CoreGetHwCommandsTemplates = dict[str, HwCommandsTemplate]


# core/reset_password_request


class CoreResetPasswordRequestParams(TypedDict):
    user: Required[str]
    url: Required[str]
    email: Required[str]


# core/reset_password_perform


class CoreResetPasswordPerformParams(TypedDict):
    user: Required[str]
    code: Required[str]


class CoreResetPasswordPerformResponse(TypedDict):
    newPassword: str


# core/batch


class CoreBatchParamsInstance(TypedDict):
    svc: Required[str]
    params: Required[Any]


class CoreBatchParams(TypedDict):
    params: Required[list[CoreBatchParamsInstance]]
    flags: Required[int]


CoreBatchResponse = list[CoreErrorCode]


# core/duplicate


class CoreDuplicateParams(TypedDict):
    operateAs: Required[str]
    continueCurrentSession: Required[bool]


CoreDuplicateResponse: Incomplete = Incomplete


# core/create_auth_hash


class CoreCreateAuthHashResponse(TypedDict):
    authHash: str


# core/use_auth_hash


class CoreUseAuthHashParams(TypedDict):
    authHash: Required[str]
    operateAs: Required[str]
    checkService: Required[str]


CoreUseAuthHashResponse: Incomplete = Incomplete


# core/check_unique


class CoreCheckUniqueParams(TypedDict):
    type: Required[str]
    value: Required[str]


class IsUnique(IntEnum):
    UNIQUE = 0
    EXISTS = 1


class CoreCheckUniqueResponse(TypedDict):
    result: IsUnique


# core/export_file
# params same as CoreSearchItemsParams
# response is .xlsx file in bytes

CoreExportFileParams = CoreSearchItemsParams  # Incomplete
CoreExportFileResponse = bytes | None


# core/set_session_property
class CoreSessionPropertyParams(TypedDict):
    prop_name: Required[Incomplete]
    prop_value: Required[Incomplete]


CoreSessionPropertyResponse: Incomplete = Incomplete
