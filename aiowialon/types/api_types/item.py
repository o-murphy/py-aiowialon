# pylint: disable=missing-module-docstring,line-too-long,missing-class-docstring
from enum import IntEnum
from typing_extensions import TypedDict, Required, Optional, Any, Dict, List, Union, Literal, NamedTuple
from aiowialon.utils.compat import StrEnum


Incomplete = Any


# item/update_name
class ItemUpdateNameParams(TypedDict):
    itemId: Required[int]
    name: Required[str]


class ItemUpdateNameResponse(TypedDict):
    nm: str


# item/delete_item

class ItemDeleteItemParams(TypedDict):
    itemId: Required[int]


ItemDeleteItemResponse = Dict[str, Any]


# item/update_custom_field

class ItemUpdateCustomFieldParams(TypedDict, total=False):
    itemId: Required[int]
    id: Required[int]
    callMode: Literal['create', 'update', 'delete']
    n: Optional[str]  # required for create and update
    v: Optional[str]  # required for create and update


class ItemUpdateCustomField(TypedDict):
    id: int
    n: str
    v: str


class ItemUpdateCustomFieldResponse(NamedTuple):
    id: int
    data: Union[ItemUpdateCustomField, None]


# item/update_custom_field

class ItemUpdateCustomPropertyParams(TypedDict):
    itemId: Required[int]
    name: Required[str]
    value: Required[Union[str, Literal[""]]]


class ItemUpdateCustomPropertyResponse(TypedDict):
    n: str
    v: str


# item/update_admin_field

ItemUpdateAdminFieldParams = ItemUpdateCustomFieldParams
ItemUpdateAdminField = ItemUpdateCustomField
ItemUpdateAdminFieldResponse = ItemUpdateCustomFieldResponse

# item/add_log_record


AddLogRecordActions = Literal[
    'custom_msg',
    'create_unit',
    'update_name',
    'update_access',
    'update_unit_icon',
    'update_unit_pass',
    'update_unit_phone',
    'update_unit_calcflags',  # (update sensor calculation settings)',
    'update_unit_milcounter',  # (update mileage counter value)',
    'update_unit_bytecounter',  # (update GPRS traffic counter value)',
    'update_unit_ehcounter',  # (update engine hours counter value)',
    'update_unit_uid',
    'update_unit_hw',  # (update device type)',
    'update_unit_hw_cfg',  # (update device configuration)',
    'update_unit_fuel_cfg',  # (update fuel consumption configuration)',
    'update_unit_trip_cfg',  # (update trip detection configuration)',
    'create_sensor',
    'update_sensor',
    'delete_sensor',
    'create_alias',  # (create command)',
    'update_alias',  # (update command)',
    'delete_alias',  # (delete command)',
    'create_service_interval',
    'update_service_interval',
    'delete_service_interval',
    'create_custom_field',
    'update_custom_field',
    'delete_custom_field',
    'import_item_cfg',
    'import_unit_cfg',
    'export_unit_msgs',
    'import_unit_msgs',
    'delete_unit_msg',
    'delete_unit_msgs',
    'bind_unit_driver',
    'unbind_unit_driver',
    'bind_unit_trailer',
    'unbind_unit_trailer',
    'update_unit_report_cfg',  # (update parameters used in reports)',
    'update_msgs_filter_cfg',  # (update filtration of unit position information in messages)',
    'delete_item',
    'create_user',
    'update_hosts_mask',
    'update_user_pass',
    'update_user_flags',
    'create_user_notify',
    'delete_user_notify',
    'create_group',
    'units_group',  # (add/remove units to/from unit group);
    'update_driver_units',  # (update the list of auto attachable units for drivers)',
    'update_trailer_units',  # (update the list of auto attachable units for trailers)',
    'create_resource',
    'create_zone',
    'update_zone',
    'delete_zone',
    'create_poi',
    'update_poi',
    'delete_poi',
    'create_job',
    'switch_job',
    'update_job',
    'delete_job',
    'create_notify',
    'switch_notify',
    'update_notify',
    'delete_notify',
    'create_driver',
    'update_driver',
    'delete_driver',
    'create_trailer',
    'update_trailer',
    'delete_trailer',
    'create_drivers_group',
    'update_drivers_group',
    'delete_drivers_group',
    'create_trailers_group',
    'update_trailers_group',
    'delete_trailers_group',
    'create_report',  # (create report template)',
    'update_report',  # (update report template)',
    'delete_report',  # (delete report template)',
    'import_pois',
    'import_zones',
    'create_retranslator',
    'update_retranslator',
    'units_retranslator',  # (add units for retranslation)',
    'switch_retranslator',
    'create_route',
    'update_route_points',
    'update_route_cfg',
    'create_round',
    'update_round',
    'delete_round',
    'create_schedule',
    'update_schedule',
    'delete_schedule',
    'create_account',
    'delete_account',
    'switch_account',
    'update_dealer_rights',
    'do_payment',
    'update_account_flags',
    'update_account_min_days',
    'update_account_plan',
    'update_account_history_period',
    'update_account_subplans',
    'create_service',
    'update_service',
    'delete_service'
]


class AddLogRecordParams(TypedDict):
    itemId: Required[int]
    action: Required[AddLogRecordActions]
    newValue: Required[str]
    oldValue: Required[str]


AddLogRecordResponse = Dict[str, Any]


# item/list_backups
class ItemListBackupsParams(TypedDict):
    itemId: Required[int]


class ItemBackup(TypedDict):
    date: str
    t: int
    unitId: int
    id: int
    name: str


class ItemListBackupsResponse(TypedDict):
    result: List[ItemBackup]


class ItemTargetMeasurement(IntEnum):
    METRIC = 0
    US = 1
    IMPERIAL = 2


# item/update_measure_units
class ItemUpdateMeasureUnitsParams(TypedDict):
    itemId: Required[int]
    type: Required[ItemTargetMeasurement]
    flags: Required[Incomplete]


ItemUpdateMeasureUnitsResponse = Dict[str, Any]


# item/update_ftp_property

class Check(IntEnum):
    NO = 0
    YES = 1


class ItemUpdateFtpPropertyParams(TypedDict):
    itemId: Required[int]
    host: Required[str]
    login: Required[str]
    pass_: Required[str]
    path: Required[str]
    check: Required[Check]
    hostingFtp: Required[Check]


class ItemUpdateFtpPropertyResponse(TypedDict):
    hs: str
    lg: str
    pt: str
    ch: int
    tp: int


# item/update_profile_field

class ProfileFieldName(StrEnum):
    VEHICLE_CLASS = 'vehicle_class'
    VIN = 'vin'
    REGISTRATION_PLATE = 'registration_plate'
    BRAND = 'brand'
    MODEL = 'model'
    YEAR = 'year'
    COLOR = 'color'
    ENGINE_MODEL = 'engine_model'
    ENGINE_POWER = 'engine_power'
    ENGINE_DISPLACEMENT = 'engine_displacement'
    PRIMARY_FUEL_TYPE = 'primary_fuel_type'
    CARGO_TYPE = 'cargo_type'
    CARRYING_CAPACITY = 'carrying_capacity'
    WIDTH = 'width'
    HEIGHT = 'height'
    DEPTH = 'depth'
    EFFECTIVE_CAPACITY = 'effective_capacity'
    GROSS_VEHICLE_WEIGHT = 'gross_vehicle_weight'
    AXLES = 'axles'
    VEHICLE_TYPE = 'vehicle_type'


class ItemUpdateProfileFieldParams(TypedDict):
    itemId: Required[int]
    n: Required[ProfileFieldName]
    v: Required[str]


ItemUpdateProfileField = ItemUpdateCustomField
ItemUpdateProfileFieldResponse = ItemUpdateCustomFieldResponse


# item/restore_icons
class ItemRestoreIconsParams(TypedDict):
    resId: Required[int]
    trailerIcons: Dict[int, str]
    driverIcons: Dict[int, str]
    zoneIcons: Dict[int, str]
    unitIcons: Dict[int, str]


ItemRestoreIconsResponse = Dict[str, Any]
