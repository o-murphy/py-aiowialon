# pylint: disable=missing-module-docstring,line-too-long,missing-class-docstring
from enum import IntEnum
from typing_extensions import TypedDict, Required, Optional, Any, Dict, List, Union, Literal
from aiowialon.types import flags

Incomplete = Any


# core/logout
class CoreErrorCode(TypedDict, total=False):
    error: int
    reason: Optional[str]


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
    cost: Optional[str]
    interval: Optional[int]


class BillingPlan(TypedDict, total=False):
    flags: int
    blockBalance: int
    denyBalance: int
    minDaysCounter: int
    historyPeriod: int
    services: Dict[str, AccountService]


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
    services: Optional[Dict[str, AccountService]]  # minimal only
    settings: Optional[AccountSettings]  # detailed only
    siteAccess: Optional[Dict[str, str]]  # detailed only
    dealerRights: int
    subPlans: List[str]
    switchTime: Optional[int]  # minimal only


# core/check_items_billing
class CoreChechItemsBillingParams(TypedDict):
    items: Required[List[int]]
    accessFlags: Required[int]
    serviceName: Required[str]


CoreChechItemsBillingResponse = List[int]


# core/check_accessors
class CoreCheckAccessorsAddDact(IntEnum):
    DONT_ADD = 0
    ADD = 1


class CoreCheckAccessorsParams(TypedDict):
    items: Required[List[int]]
    flags: Required[CoreCheckAccessorsAddDact]


class CoreCheckAccessorsAccessRights(TypedDict, total=False):
    acl: int
    dacl: int


CoreCheckAccessorsResponse = Dict[str, Dict[str, CoreCheckAccessorsAccessRights]]


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
    auth: Optional[str]
    ssl: Optional[bool]  # for NIS
    debug: Required[bool]
    v6type: Optional[bool]  # for GRANIT_NAVIGATOR only


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
    propType: Optional[str]
    or_logic: Optional[bool]


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
    items: List[Incomplete]


# core/update_data_flags
class CoreUpdateDataFlagsSpec(TypedDict, total=False):
    type: Required[Incomplete]
    data: Required[Union[str, int, List[int]]]
    flags: Required[flags.UnitsDataFlag]
    mode: Required[Incomplete]
    max_items: Optional[int]


class CoreUpdateDataFlagsParams(TypedDict):
    spec: Required[List[CoreUpdateDataFlagsSpec]]


class CoreUpdateDataFlagsResponse(TypedDict):
    i: int
    d: Dict[str, Incomplete]
    f: int


# core/get_hw_types

HwCategory = Literal['auto', 'tracker', 'mobile', 'soft']
HwFeature = Literal['wifi_pos']

CoreGetHwTypesFilterType = Literal['name', 'id', 'type', 'feature']
CoreGetHwTypesFilter = Union[str, int, List[int], HwCategory, HwFeature]


class CoreGetHwTypesParams(TypedDict):
    filterType: Required[CoreGetHwTypesFilterType]
    filterValue: Required[CoreGetHwTypesFilter]
    includeType: Required[Union[int, bool]]
    ignoreRename: Required[Union[int, bool]]


class CoreHwType(TypedDict, total=False):
    id: int
    uid2: int
    name: str
    hw_category: Optional[HwCategory]
    tp: int
    up: int


CoreGetHwTypesResponse = List[CoreHwType]


# core/get_hw_cmds

class CoreGetHwCommandsParams(TypedDict, total=False):
    deviceTypeId: Required[int]
    unitId: Optional[int]
    template: Required[bool]
    lang: Optional[Incomplete]


CoreGetHwCommandsList = Dict[Incomplete, List[Incomplete]]


class HwCommandsTemplate(TypedDict):
    icon: str
    props: List[Incomplete]


CoreGetHwCommandsTemplates = Dict[str, HwCommandsTemplate]


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
    params: Required[List[CoreBatchParamsInstance]]
    flags: Required[int]


CoreBatchResponse = List[CoreErrorCode]


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
CoreExportFileResponse = Union[bytes, None]


# core/set_session_property
class CoreSessionPropertyParams(TypedDict):
    prop_name: Required[Incomplete]
    prop_value: Required[Incomplete]


CoreSessionPropertyResponse: Incomplete = Incomplete
