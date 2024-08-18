# pylint: disable=missing-module-docstring,line-too-long,missing-class-docstring
from enum import IntEnum, IntFlag
from typing_extensions import TypedDict, Required, Optional, Any, Dict, Union, Tuple

Incomplete = Any


# user/verify_auth
class AddressType(IntEnum):
    SMS = 0
    EMAIL = 1


class UserVerifyAuthParams(TypedDict):
    userId: Required[int]
    type: Required[AddressType]
    destination: Required[str]


class UserVerifyAuthResponse(TypedDict):
    code: str


# user/update_auth_params
class UserUpdateAuthParamsParams(TypedDict, total=False):
    userId: Required[int]
    type: Required[AddressType]
    destination: Optional[str]


class UserUpdateAuthParamsResponse(TypedDict):
    type: int
    phone: str


# user/update_item_access
class UserUpdateItemAccessParams(TypedDict):
    userId: Required[str]
    itemId: Required[str]
    accessMask: Required[Incomplete]


UserUpdateItemAccessResponse = Dict[str, Any]


# user/get_items_access&params
class ItemSuperclassType(IntEnum):
    # Define item superclass types, example values; adjust as necessary
    OBJECT = 0
    USER = 1
    GROUP = 2


class UserGetItemsAccessParams(TypedDict, total=False):
    userId: Required[int]
    directAccess: Required[bool]
    itemSuperclass: Required[str]
    flags: Optional[int]


class UserGetItemsAccessResponseItem(TypedDict):
    cacl: int  # combined access level
    dacl: int  # direct access level


UserGetItemsAccessResponse = Dict[str, Union[int, UserGetItemsAccessResponseItem]]


# user/update_hosts_mask
class UserUpdateHostsMaskParams(TypedDict):
    userId: Required[int]
    hostsMask: Required[str]


class UserUpdateHostsMaskResponse(TypedDict):
    hm: str  # host mask


# user/update_user_notification
class NotificationHead(TypedDict):
    c: int  # color, RGB
    fs: str  # font size


class NotificationMessage(TypedDict):
    body: str  # message body
    head: NotificationHead
    multiple: int  # 1 for multiple activation, 0 for single activation


class UserUpdateUserNotificationParams(TypedDict, total=False):
    itemId: Required[int]  # user ID
    id: Required[int]  # notice ID, required for delete
    callMode: Required[str]  # action: 'create', 'delete'
    h: Optional[str]  # subject, required for create/update
    d: Optional[NotificationMessage]  # message text settings, required for create/update
    s: Optional[str]  # sender, required for create/update
    ttl: Optional[int]  # lifetime (UTC in millisecs from 1 Jan 1970), required for create/update


class UserUpdateUserNotificationResponseCreateItem(TypedDict):
    id: int  # notice ID
    t: int  # lifetime (UTC)
    d: str  # message text settings
    h: str  # subject
    s: str  # sender


UserUpdateUserNotificationResponse = Tuple[int, Union[Any, UserUpdateUserNotificationResponseCreateItem]]


# user/update_password
class UserUpdatePasswordParams(TypedDict):
    userId: Required[int]  # user ID
    oldPassword: Required[str]  # old password
    newPassword: Required[str]  # new password


UserUpdatePasswordResponse = Dict[str, Any]


# user/send_sms
class UserSendSmsParams(TypedDict):
    phoneNumber: Required[str]  # phone number
    smsText: Required[str]  # SMS message text


UserSendSmsResponse = Dict[str, Any]  # empty object if execution is successful


class UserSendSmsErrorCodes(IntEnum):
    ERROR_SENDING_SMS = 6  # error sending SMS


# user/update_user_flags
class UserUpdateUserFlags(IntFlag):
    USER_DISABLED = 0x01  # User disabled
    CANT_CHANGE_PASSWORD = 0x02  # Can't change password
    CAN_CREATE_ITEMS = 0x04  # Can create items
    CANT_CHANGE_SETTINGS = 0x10  # Can't change settings
    CAN_SEND_SMS = 0x20  # Can send SMS


class UserUpdateUserFlagsParams(TypedDict):
    userId: Required[int]  # user ID
    flags: Required[UserUpdateUserFlags]  # settings flags
    flagsMask: Required[int]  # mask that determines which bits will be changed


class UserUpdateUserFlagsResponse(TypedDict):
    fl: int  # updated flags


# user/update_locale
class Locale(TypedDict):
    fd: Required[str]  # date and time format
    wd: Required[int]  # first week day (1 for Monday, 7 for Sunday)


class UserUpdateLocaleParams(TypedDict):
    userId: Required[int]  # user ID
    locale: Required[Locale]  # locale settings


class UserUpdateLocaleResponse(TypedDict):
    locale: Locale  # response with updated locale settings


# user/get_locale
class UserGetLocaleResponseChanged(TypedDict):
    fd: str  # date and time format
    wd: int  # first week day (1 for Monday, 7 for Sunday)


class UserGetLocaleParams(TypedDict):
    userId: Required[int]  # user ID


UserGetLocaleResponse = Union[UserGetLocaleResponseChanged, Dict[str, Any]]  # either settings or blank object


# user/get_dst_time
class UserGetDstTimeParams(TypedDict):
    timeFrom: Required[int]  # time from, UNIX time
    timeTo: Required[int]  # time to, UNIX time
    tz: int  # time zone (optional)


UserGetDstTimeResponse = Dict[str, int]  # keys are dynamic text, values are UNIX times (1 for DST start, 0 for DST end)
