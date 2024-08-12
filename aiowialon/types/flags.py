"""Enumerators of Wialon ACL Flags, Request and Response Data Flags."""

from enum import IntFlag, IntEnum
from aiowialon.utils.compat import StrEnum

# pylint: disable=line-too-long,missing-class-docstring


class ItemType(StrEnum):
    AVL_HW = 'avl_hw'
    AVL_RESOURCE = 'avl_resource'
    AVL_RETRANSLATOR = 'avl_retranslator'
    AVL_UNIT = 'avl_unit'
    AVL_UNIT_GROUP = 'avl_unit_group'
    USER = 'user'
    AVL_ROUTE = 'avl_route'


class ItemProp(StrEnum):
    SYS_NAME = "sys_name"  # item name;
    SYS_ID = "sys_id"  # item ID;
    SYS_UNIQUE_ID = "sys_unique_id"  # unique unit ID (IMEI);
    SYS_PHONE_NUMBER = "sys_phone_number"  # unit phone number;
    SYS_PHONE_NUMBER2 = "sys_phone_number2"  # unit second phone number;
    SYS_USER_CREATOR = "sys_user_creator"  # creator ID;
    REL_USER_CREATOR_NAME = "rel_user_creator_name"  # creator name;
    SYS_BILLING_ACCOUNT_GUID = "sys_billing_account_guid"  # account ID;
    REL_BILLING_ACCOUNT_NAME = "rel_billing_account_name"  # account name;
    REL_BILLING_PARENT_ACCOUNT_NAME = "rel_billing_parent_account_name"  # parent account name;
    REL_BILLING_PLAN_NAME = "rel_billing_plan_name"  # billing plan name;
    SYS_COMM_STATE = "sys_comm_state"  # hardware state (1 = "1" #  enabled, 0 = "0" #  disabled);
    REL_HW_TYPE_NAME = "rel_hw_type_name"  # hardware name;
    REL_HW_TYPE_ID = "rel_hw_type_id"  # hardware ID;
    SYS_ACCOUNT_BALANCE = "sys_account_balance"  # account balance;
    SYS_ACCOUNT_DAYS = "sys_account_days"  # account days;
    SYS_ACCOUNT_ENABLE_PARENT = "sys_account_enable_parent"  # dealer rights (1 = "1" #  on, 0 = "0" #  off);
    SYS_ACCOUNT_DISABLED = "sys_account_disabled"  # account blocked (1 = "1" #  blocked);
    # last modification time for sys_account_disabled, UNIX-time;
    REL_ACCOUNT_DISABLED_MOD_TIME = "rel_account_disabled_mod_time"
    REL_ACCOUNT_UNITS_USAGE = "rel_account_units_usage"  # number of units used in account;
    REL_LAST_MSG_DATE = "rel_last_msg_date"  # last message time, UNIX-time;
    REL_IS_ACCOUNT = "rel_is_account"  # whether resource is account (1 = "1" #  yes, 0 = "0" #  no);
    LOGIN_DATE = "login_date"  # last login time, UNIX-time;
    RETRANSLATOR_ENABLED = "retranslator_enabled"  # whether retranslator enabled ( 1 = "1" #  yes, 0 = "0" #  no);
    REL_CREATION_TIME = "rel_creation_time"  # creation time;
    REL_GROUP_UNIT_COUNT = "rel_group_unit_count"  # the number of units in a group;
    REL_CUSTOM_FIELD_NAME = "rel_customfield_name"  # the name of unit custom field;
    REL_CUSTOM_FIELD_VALUE = "rel_customfield_value"  # the eid of unit custom field;
    PROFILE_FIELD = "profilefield"  # the unit profile field (eid);
    REL_PROFILE_FIELD_NAME = "rel_profilefield_name"  # the name of unit profile field;
    REL_PROFILE_FIELD_VALUE = "rel_profilefield_value"  # the eid of unit profile field;
    REL_ADMIN_FIELD_NAME = "rel_adminfield_name"  # the name of unit admin field;
    REL_ADMIN_FIELD_VALUE = "rel_adminfield_value"  # the eid of unit admin field;
    # the name and eid of unit custom field, separated by “:”;
    REL_CUSTOM_FIELD_NAME_VALUE = "rel_customfield_name_value"
    # the name and eid of unit profile field, separated by “:”;
    REL_PROFILE_FIELD_NAME_VALUE = "rel_profilefield_name_value"
    # the name and eid of unit admin field, separated by “:”.
    REL_ADMIN_FIELD_NAME_VALUE = "rel_adminfield_name_value"


class ItemPropType(StrEnum):
    PROPERTY = "property"
    LIST = 'list'
    PROP_ITEM_NAME = 'propitemname'
    CREATOR_TREE = 'creatortree'
    ACCOUNT_TREE = 'accounttree'
    CUSTOM_FIELD = 'customfield'
    PROFILE_FIELD = 'profilefield'
    ADMIN_FIELD = 'adminfield'
    _REL_PROFILE_FIELD_NAME_VALUE = "rel_profilefield_name_value"


class AvlUnitSubItem(StrEnum):
    UNIT_SENSORS = "unit_sensors"
    UNIT_COMMANDS = "unit_commands"
    SERVICE_INTERVALS = "service_intervals"

    CUSTOM_FIELDS = "custom_fields"
    ADMIN_FIELDS = "admin_fields"


class AvlResourceSubItem(StrEnum):
    DRIVERS = "drivers"
    DRIVER_GROUPS = "driver_groups"
    JOBS = "jobs"
    NOTIFICATIONS = "notifications"
    POIS = "pois"
    TRAILERS = "trailers"
    TRAILER_GROUPS = "trailer_groups"
    ZONES_LIBRARY = "zones_library"
    REPORT_TEMPLATES = "report_templates"
    ORDERS = "orders"

    CUSTOM_FIELDS = "custom_fields"
    ADMIN_FIELDS = "admin_fields"


class AvlRouteSubItem(StrEnum):
    ROUNDS = "rounds"
    ROUTE_SCHEDULES = "route_schedules"


class AvlRetranslatorSubItem(StrEnum):
    RETRANSLATOR_UNITS = "retranslator_units"


class AvlUserSubItem(StrEnum):
    CUSTOM_FIELDS = "custom_fields"
    ADMIN_FIELDS = "admin_fields"


# pylint: disable=implicit-flag-alias
class ItemDataFlag(IntFlag):
    # Base item information
    BASE = 0x00000001
    # Item custom properties
    CUSTOM_PROPS = 0x00000002
    # Item billing/construction properties
    BILLING_PROPS = 0x00000004
    # Item custom fields
    CUSTOM_FIELDS = 0x00000008
    # Item image
    IMAGE = 0x00000010
    # Item messages
    MSGS = 0x00000020
    # Item GUID
    GUID = 0x00000040
    # Admin fields plugin
    ADMIN_FIELDS = 0x00000080

    ALL = 0x3FFFFFFFFFFFFFFF  # set all possible flags to item


class UnitsDataFlag(IntFlag):
    BASE = ItemDataFlag.BASE
    CUSTOM_PROPS = ItemDataFlag.CUSTOM_PROPS
    BILLING_PROPS = ItemDataFlag.BILLING_PROPS
    CUSTOM_FIELDS = ItemDataFlag.CUSTOM_FIELDS
    IMAGE = ItemDataFlag.IMAGE
    MSGS = ItemDataFlag.MSGS
    GUID = ItemDataFlag.GUID
    ADMIN_FIELDS = ItemDataFlag.ADMIN_FIELDS

    ALL = ItemDataFlag.ALL

    ADVANCED_PROPS = 0x00000100  # 256, advanced properties
    AVAILABLE_CMDS = 0x00000200  # 512, available for current moment commands
    LAST_MSG_N_POS = 0x00000400  # 1024, last message and position
    SENSORS = 0x00001000  # 4096, sensors
    COUNTERS = 0x00002000  # 8192, counters
    MAINTENANCE = 0x00008000  # 32768, maintenance
    UNIT_CONFIG_IN_REPORTS = 0x00020000  # 131072, unit configuration in reports: trip detector and fuel consumption
    POSSIBLE_CMDS = 0x00080000  # 524288, list of all possible commands for current unit
    MSG_PARAMETERS = 0x00100000  # 1048576, message parameters
    UNIT_CONNECTION_STATUS = 0x00200000  # 2097152, unit connection status
    POS = 0x00400000  # 4194304, position
    PROFILE_FIELDS = 0x00800000  # 8388608, profile fields


class UnitGroupsDataFlag(IntFlag):
    BASE = ItemDataFlag.BASE
    CUSTOM_PROPS = ItemDataFlag.CUSTOM_PROPS
    BILLING_PROPS = ItemDataFlag.BILLING_PROPS
    CUSTOM_FIELDS = ItemDataFlag.CUSTOM_FIELDS
    IMAGE = ItemDataFlag.IMAGE
    MSGS = ItemDataFlag.MSGS
    GUID = ItemDataFlag.GUID
    ADMIN_FIELDS = ItemDataFlag.ADMIN_FIELDS

    ALL = ItemDataFlag.ALL


class UserDataFlag(IntFlag):
    BASE = ItemDataFlag.BASE
    CUSTOM_PROPS = ItemDataFlag.CUSTOM_PROPS
    BILLING_PROPS = ItemDataFlag.BILLING_PROPS
    CUSTOM_FIELDS = ItemDataFlag.CUSTOM_FIELDS
    IMAGE = ItemDataFlag.IMAGE
    MSGS = ItemDataFlag.MSGS
    GUID = ItemDataFlag.GUID
    ADMIN_FIELDS = ItemDataFlag.ADMIN_FIELDS

    ALL = ItemDataFlag.ALL

    OTHER_PROPS = 0x00000100  # 256, other properties
    NOTIFS = 0x00000200  # 512, notifications


class ResourceDataFlag(IntFlag):
    BASE = ItemDataFlag.BASE
    CUSTOM_PROPS = ItemDataFlag.CUSTOM_PROPS
    BILLING_PROPS = ItemDataFlag.BILLING_PROPS
    CUSTOM_FIELDS = ItemDataFlag.CUSTOM_FIELDS
    IMAGE = ItemDataFlag.IMAGE
    MSGS = ItemDataFlag.MSGS
    GUID = ItemDataFlag.GUID
    ADMIN_FIELDS = ItemDataFlag.ADMIN_FIELDS

    ALL = ItemDataFlag.ALL

    DRIVERS = 0x00000100  # 256, drivers
    JOBS = 0x00000200  # 512, jobs
    NOTIFS = 0x00000400  # 1024, notifications
    POIS = 0x00000800  # 2048, POIs
    GEOFENCES = 0x00001000  # 4096, geofences
    REPORT_TEMPLATES = 0x00002000  # 8192, report templates
    AUTO_ATTACHABLE_UNITS_FOR_DRIVERS = 0x00004000  # 16384, list of auto attachable units for drivers
    DRIVER_GROUPS = 0x00008000  # 32768, driver groups
    TRAILERS = 0x00010000  # 65536, trailers
    TRAILER_GROUPS = 0x00020000  # 131072, trailer groups
    AUTO_ATTACHABLE_UNITS_FOR_TRAILERS = 0x00040000  # 262144, list of auto attachable units for trailers
    ORDERS = 0x00080000  # 524288, orders
    GEOFENCES_GROUPS = 0x00100000  # 1048576, geofences groups
    TAGS = 0x00200000  # 2097152, tags (passengers)
    AUTOMATIC_UNITS_BINDING_FOR_TAGS = 0x00400000  # 4194304, automatic binding list of units (for tags)
    TAGS_GROUPS = 0x00800000  # 8388608, tags groups(passengers)


class RouteDataFlag(IntFlag):
    BASE = ItemDataFlag.BASE
    CUSTOM_PROPS = ItemDataFlag.CUSTOM_PROPS
    BILLING_PROPS = ItemDataFlag.BILLING_PROPS
    CUSTOM_FIELDS = ItemDataFlag.CUSTOM_FIELDS
    IMAGE = ItemDataFlag.IMAGE
    MSGS = ItemDataFlag.MSGS
    GUID = ItemDataFlag.GUID
    ADMIN_FIELDS = ItemDataFlag.ADMIN_FIELDS

    ALL = ItemDataFlag.ALL

    CONFIG = 0x00000100  # 256, configuration
    CHECK_POINTS = 0x00000200  # 512, check points
    SCHEDULES = 0x00000400  # 1204, schedules
    ROUNDS = 0x00000800  # 2048, rounds


class RetranslatorDataFlag(IntFlag):
    BASE = ItemDataFlag.BASE
    CUSTOM_PROPS = ItemDataFlag.CUSTOM_PROPS
    BILLING_PROPS = ItemDataFlag.BILLING_PROPS
    CUSTOM_FIELDS = ItemDataFlag.CUSTOM_FIELDS
    IMAGE = ItemDataFlag.IMAGE
    MSGS = ItemDataFlag.MSGS
    GUID = ItemDataFlag.GUID
    ADMIN_FIELDS = ItemDataFlag.ADMIN_FIELDS

    ALL = ItemDataFlag.ALL

    STATE_N_CONFIG = 0x00000100  # 256, state and configuration
    UNITS = 0x00000200  # 512, units


class MessageTypeFlag(IntFlag):
    """
    In order to delete specific messages you must have the following ACL-flags:

        What to delete  Message flag HEX(DEC)	ACL-flag HEX(DEC)
        Data message	0x0000(0)	0x800000(8388608)
        SMS	0x0100(256)	0x800000(8388608)
        Command	0x0200(512)	0x800000(8388608)
        Event	0x0600(1536)	0x2000000(33554432)
        Log	0x1000(4096)	0x800(2048)
    """

    UNIT_MSGS_WITH_DATA = 0x0000  # 0, messages with data
    UNIT_SMS = 0x0100  # 256, SMS
    UNIT_CMD = 0x0200  # 512, command
    UNIT_EVENT = 0x0600  # 1536, event
    UNIT_VIDEO_USAGE = 0x2000  # 8192, video usage

    RESOURCE_NOTIFICATION = 0x0300  # 768, notification
    RESOURCE_BILLING_MSG = 0x0500  # 1280, billing message
    RESOURCE_SMS_FOR_DRIVER = 0x0900  # 2304, SMS for driver

    LOG_MSGS = 0x1000  # 4096, Log messages


class MessagesWithDataFlags(IntFlag):
    HAS_POS_INFO = 0x01  # 1, position information is available
    HAS_INPUT_DATA = 0x02  # 2, input data information is available
    HAS_OUTPUT_DATA = 0x04  # 4, output data information is available
    HAS_STATE_INFO = 0x08  # 8, state information is available
    HAS_ALARM_BIT = 0x10  # 16, message contains alarm bit
    # 32, message contains information about driver code which come only in parameter avl_driver
    HAS_AVL_DRIVER_CODE = 0x20
    WAS_CORRECTED_BY_LBS = 0x20000  # 131072, message was corrected by lbs
    HAS_WIFI_POS = 0x80000  # 524288, message contains wi-fi position


class MessagesEventTypeFlags(IntFlag):
    SIMPLE = 0x0  # 0, simple event
    VIOLATION = 0x1  # 1, violation
    MAINTENANCE = 0x2  # 2, maintenance event
    ROUTE_CTRL = 0x4  # 4, route control event
    MAINTENANCE_IS_REGISTERED = 0x10  # 16, is set in addition to flag 0x2: maintenance is registered
    REGISTERED_FILLING = 0x20  # 32, is set in addition to flag 0x2: registered filling


# pylint: disable=implicit-flag-alias
class AccessControlFlags(IntFlag):
    VIEW_BASIC_PROPS = 0x0001  # View item and its basic properties
    VIEW_DETAILED_PROPS = 0x0002  # View detailed item properties
    MANAGE_ACCESS = 0x0004  # Manage access to this item
    DEL_ITEM = 0x0008  # Delete item
    RENAME_ITEM = 0x0010  # Rename item
    VIEW_CUSTOM_FIELDS = 0x0020  # View custom fields
    MANAGE_CUSTOM_FIELDS = 0x0040  # Manage custom fields
    EDIT_NOT_MENTIONED_PROPS = 0x0080  # Edit not mentioned properties
    CHANGE_ICON = 0x0100  # Change icon
    QUERY_REPORTS_OR_MSGS = 0x0200  # Query reports or messages
    EDIT_ACL_PROPAGATED_ITEMS = 0x0400  # Edit ACL propagated items
    MANAGE_ITEM_LOG = 0x0800  # Manage item log
    VIEW_ADMIN_FIELDS = 0x1000  # View administrative fields
    EDIT_ADMIN_FIELDS = 0x2000  # Edit administrative fields
    VIEW_ATTACHED_FILES = 0x4000  # View attached files
    EDIT_ATTACHED_FILES = 0x8000  # Edit attached files

    # UnitsAndGroups

    # # Edit connectivity settings (device type, UID, phone, access password, messages filter)
    EDIT_CONNECT_SETTINGS = 0x0000100000
    CRUD_SENSORS = 0x0000200000  # Create, edit, and delete sensors
    EDIT_COUNTERS = 0x0000400000  # Edit counters
    DEL_MSGS = 0x0000800000  # Delete messages
    EXECUTE_CMDS = 0x0001000000  # Execute commands
    REGISTER_EVENTS = 0x0002000000  # Register events
    # # View connectivity settings (device type, UID, phone, access password, messages filter)
    VIEW_CONNECT_SETTINGS = 0x0004000000
    VIEW_SERVICE_INTERVALS = 0x0010000000  # View service intervals
    CRUD_SERVICE_INTERVALS = 0x0020000000  # Create, edit, and delete service intervals
    IMPORT_MSGS = 0x0040000000  # Import messages
    EXPORT_MSGS = 0x0080000000  # Export messages
    VIEW_CMDS = 0x0400000000  # View commands
    CRUD_CMDS = 0x0800000000  # Create, edit, and delete commands
    EDIT_TRIP_DETECTOR_N_FUEL_CONSUMPTION = 0x4000000000  # Edit trip detector and fuel consumption
    # # Use unit in jobs, notifications, routes, retranslators
    USE_UNIT_IN_JOBS_NOTIFS_ROUTES_RETRANSLATORS = 0x8000000000

    # Users
    MANAGE_USER_ACCESS_RIGHTS = 0x100000  # Manage user`s access rights
    ACT_AS_GIVEN_USER = 0x200000  # Act as given user (create items, login, etc.)
    CHANGE_FLAGS_FOR_GIVEN_USER = 0x400000  # Change flags for given user
    VIEW_PUSH_MSGS = 0x800000  # View push messages for mobile app
    EDIT_PUSH_MSGS = 0x1000000  # Edit push messages

    # Retranslators
    EDIT_RETRANSLATOR_PROPS_CTRL = 0x100000  # Edit retranslator properties including start/stop
    MANAGE_UNITS_IN_RETRANSLATOR = 0x200000  # Add or remove units from retranslator, change their UIDs

    # Resources
    VIEW_NOTIFS = 0x0000000100000  # View notifications
    CRUD_NOTIFS = 0x0000000200000  # Create, edit, and delete notifications
    VIEW_POIS = 0x0000000400000  # View POIs
    CRUD_POIS = 0x0000000800000  # Create, edit, and delete POIs
    VIEW_GEOFENCES = 0x0000001000000  # View geofences
    CRUD_GEOFENCES = 0x0000002000000  # Create, edit, and delete geofences
    VIEW_JOBS = 0x0000004000000  # View jobs
    CRUD_JOBS = 0x0000008000000  # Create, edit, and delete jobs
    VIEW_REPORT_TEMPLATES = 0x0000010000000  # View report templates
    CRUD_REPORT_TEMPLATES = 0x0000020000000  # Create, edit, and delete report templates
    VIEW_DRIVERS_N_GROUPS = 0x0000040000000  # View drivers and driver groups
    CRUD_DRIVERS_N_GROUPS = 0x0000080000000  # Create, edit, and delete drivers and driver groups
    MANAGE_ACCOUNT = 0x0000100000000  # Manage account
    VIEW_ORDERS = 0x0000200000000  # View orders
    CRUD_ORDERS = 0x0000400000000  # Create, edit, and delete orders
    VIEW_PASSENGERS_N_GROUPS = 0x0000800000000  # View passengers and passengers groups
    CRUD_PASSENGERS_N_GROUPS = 0x0001000000000  # Create, edit, and delete passengers and passengers groups
    VIEW_TRAILERS_N_GROUPS = 0x0100000000000  # View trailers and trailer groups
    CRUD_TRAILERS_N_GROUPS = 0x0200000000000  # Create, edit, and delete trailers and trailer groups

    # Routes
    EDIT_ROUTE_PROPS = 0x0000000100000  # Edit route properties

    # OTHER
    ALL = 0xfffffffffffffff  # Sets all possible access flags to an item


class TokenFlag(IntFlag):
    # Online tracking

    # # General
    VIEW_ITEM_N_ITS_BASIC_PROPS = 1  # 0x1, View item and its basic properties
    VIEW_DETAILED_ITEM_PROPS = 2  # 0x2, View detailed item properties
    VIEW_CUSTOM_FIELDS = 32  # 0x20, View custom fields
    QUERY_REPORTS_OR_MSGS = 512  # 0x200, Query reports or messages
    VIEW_ATTACHED_FILES = 16384  # 0x4000, View attached files

    # # Units and unit groups
    VIEW_CMDS = 17179869184  # 0x400000000, View commands

    # # Resources (Accounts)
    VIEW_POIS = 4194304  # 0x400000, View POIs
    VIEW_GEOFENCES = 16777216  # 0x1000000, View geofences
    VIEW_REPORT_TEMPLATES = 268435456  # 0x10000000, View report templates
    VIEW_DRIVERS_N_GROUPS = 1073741824  # 0x40000000, View drivers and driver groups
    VIEW_ORDERS = 8589934592  # 0x200000000, View orders
    VIEW_TAGS = 34359738368  # 0x800000000, View tags (passengers)
    VIEW_TRAILERS_N_GROUPS = 17592186044416  # 0x100000000000, View trailers and trailer groups

    # View access to most data

    # # Units and unit groups
    VIEW_SERVICE_INTERVALS = 268435456  # 0x10000000, View service intervals
    VIEW_CONNECTIVITY_SETTINGS = 67108864  # 0x0004000000, View connectivity settings

    # # Users
    ACT_AS_GIVEN_USER = 2097152  # 0x200000, Act as given user (create items, login, etc.)

    # # Resources (Accounts)
    VIEW_NOTIFS = 1048576  # 0x100000, View notifications
    VIEW_JOBS = 67108864  # 0x4000000, View jobs

    # Modification of non-sensitive data

    # # General
    RENAME_ITEM = 16  # 0x10, Rename item
    MANAGE_CUSTOM_FIELDS = 64  # 0x40, Manage custom fields
    EDIT_NOT_MENTIONED_PROPS = 128  # 0x80, Edit not mentioned properties
    CHANGE_ICON = 256  # 0x100, Change icon
    EDIT_ATTACHED_FILES = 32768  # 0x8000, Edit attached files

    # # Units and unit groups
    REGISTER_EVENTS = 33554432  # 0x2000000, Register events
    CRUD_CMDS = 34359738368  # 0x800000000, Create, edit, and delete commands

    # # Retranslators
    MANAGE_UNITS_IN_RETRANSLATOR = 2097152  # 0x200000, Add or remove units from retranslator, change their UIDs

    # # Resources (Accounts)
    CRUD_POIS = 8388608  # 0x800000, Create, edit, and delete POIs
    CRUD_GEOFENCES = 33554432  # 0x2000000, Create, edit, and delete geofences

    # Modification of sensitive data

    # # General
    MANAGE_ACCESS_TO_THIS_ITEM = 4  # 0x4, Manage access to this item

    # # Units and unit groups
    CRUD_SERVICE_INTERVALS = 536870912  # 0x20000000, Create, edit, and delete service intervals
    EDIT_TRIP_DETECTOR_N_FUEL_CONSUMPTION = 274877906944  # 0x4000000000, Edit trip detector and fuel consumption

    # # Users
    MANAGE_USER_ACCESS_RIGHTS = 1048576  # 0x100000, Manage user`s access rights
    CHANGE_FLAGS_FOR_GIVEN_USER = 4194304  # 0x400000, Change flags for given user

    # # Retranslators
    EDIT_RETRANSLATOR_PROPS_CTRL = 1048576  # 0x100000, Edit retranslator properties including start/stop

    # # Resources (Accounts)
    CRUD_NOTIFS = 2097152  # 0x200000, Create, edit, and delete notifications
    CRUD_JOBS = 134217728  # 0x8000000, Create, edit, and delete jobs
    CRUD_REPORT_TEMPLATES = 536870912  # 0x20000000, Create, edit, and delete report templates
    CRUD_DRIVERS_N_GROUPS = 2147483648  # 0x80000000, Create, edit, and delete drivers and drivergroups
    CRUD_ORDERS = 17179869184  # 0x400000000, Create, edit, and delete orders
    CRUD_TAGS = 68719476736  # 0x1000000000, Create, edit, and delete tags (passengers)
    CRUD_TRAILERS_N_GROUPS = 35184372088832  # 0x200000000000, Create, edit, and delete trailers and trailer groups

    # Modification of critical data, including messages deletion

    # # General
    DEL_ITEM = 8  # 0x8, Delete item
    MANAGE_ITEM_LOG = 2048  # 0x800, Manage item log
    VIEW_ADMIN_FIELDS = 4096  # 0x1000, View administrative fields
    EDIT_ADMIN_FIELDS = 8192  # 0x2000, Edit administrative fields

    # # Units and unit groups
    # 0x100000, Edit connectivity settings (device type, UID, phone, access password, messages filter)
    EDIT_CONNECT_SETTINGS = 1048576
    CRUD_SENSORS = 2097152  # 0x200000, Create, edit, and delete sensors
    EDIT_COUNTERS = 4194304  # 0x400000, Edit counters
    DEL_MSGS = 8388608  # 0x800000, Delete messages
    IMPORT_MSGS = 1073741824  # 0x40000000, Import messages
    EXPORT_MSGS = 2147483648  # 0x80000000, Export messages

    # Communication (Units and unit groups)
    EXECUTE_CMDS = 16777216  # 0x1000000, Execute commands

    # Unlimited operation as authorized user
    EDIT_ACL_PROPAGATED_ITEMS = 1024  # 0x400, Edit ACL propagated items
    VIEW_ROUTES = 67108864  # 0x4000000, View routes
    CRUD_ROUTES = 134217728  # 0x8000000, Create, edit, delete routes
    VIEW_EVENTS = 68719476736  # 0x1000000000, View events
    CRUD_EVENTS = 137438953472  # 0x2000000000, Create, edit, and delete events
    # # 0x8000000000, Use unit in jobs, notifications, routes, retranslators
    USE_UNIT_IN_JOBS_NOTIFS_ROUTES_RETRANSLATORS = 549755813888
    MANAGE_ACCOUNT = 4294967296  # 0x100000000, Manage account


class BatchFlag(IntEnum):
    EXECUTE_ALL = 0
    STOP_ON_ERROR = 1


class ReportColumnValueType(IntEnum):
    """
    Refetence to https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/report/value_types

    0	Unspecified text value
    1	Address value
    2	Unspecified custom <int> value
    3	Unspecified custom <double> value
    4	Counter value
    10	Distance, in meters
    20	Speed, in km/h
    30	Time value (YYYY/MM/DD HH:MM:SS)
    31	Time value (HH:MM::SS)
    32	Time value (YYYY/MM/DD)
    40	Time interval value, in seconds
    41	Time interval value, in hours
    42	Time interval value, in hours with 2 decimal places
    50	Volume, in litres
    51	Consumption, in litres/100km
    52	Consumption, in litres/h
    53	Consumption, in litres/ha
    60	Percentage value
    70	Area in hectares
    72	Area in square meters
    80	Information measurement - bytes, kbytes, mbytes
    """
    UNEXPECTED_TEXT_VALUE = 0
    ADDRESS_VALUE = 1
    """Operation completed successfully."""

    UNSPECIFIED_CUSTOM_INT_VALUE = 2
    UNSPECIFIED_CUSTOM_DOUBLE_VALUE = 3
    COUNTER_VALUE = 4
    DISTANCE_IN_METERS = 10
    SPEED_IN_KMH = 20
    TIME_YYYY_MM_DD__HH_MM_SS = 30
    TIME_HH_MM_SS = 31
    TIME_YYYY_MM_DD = 32
    TIME_INTERVAL_VALUE_S = 40
    TIME_INTERVAL_VALUE_H = 41
    TIME_INTERVAL_VALUE_HH = 42
    VOLUME_IN_LITRES = 50
    CONSUMPTION_LITRES_PER_100KM = 51
    CONSUMPTION_LITRES_PER_H = 52
    CONSUMPTION_LITRES_PER_HA = 53
    PERCENTAGE_VALUE = 60
    AREA_IN_HA = 70
    AREA_IN_SQUARE_METERS = 72
    INFO_MEASUREMENT = 80
