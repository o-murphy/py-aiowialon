# pylint: disable=missing-module-docstring,line-too-long,missing-class-docstring
from enum import IntEnum

from typing_extensions import Any, Required, TypedDict

Incomplete = Any

# messages/unload
MessagesUnloadResponse = dict[str, Any]


# messages/delete_message
class MessagesDeleteMessageParams(TypedDict):
    msgIndex: Required[int]  # message index


class MessagesDeleteMessageResponse(TypedDict):
    pass  # empty object if execution is successful


class MessagesDeleteMessageErrorCodes(IntEnum):
    NO_SUCH_MESSAGE_OR_CANNOT_DELETE_LAST = (
        4  # No such message or this message is the last one and cannot be deleted
    )
    ERROR_DELETING_MESSAGE = 6  # Error deleting message


# messages/get_messages
class Position(TypedDict):
    y: float | None
    x: float | None
    z: float | None
    s: int | None
    c: int | None
    sc: int | None


class Parameters(TypedDict):
    adc1: int | None
    pre2: int | None
    param: int | None
    param5: int | None


class Message(TypedDict):
    t: int  # timestamp
    f: int  # some flag
    tp: str  # message type
    pos: Position  # position details
    i: int  # index or ID
    o: int  # some other field
    p: Parameters  # parameters


class MessagesGetMessagesParams(TypedDict):
    indexFrom: Required[int]  # index of the first message requested
    indexTo: Required[int]  # index of the last message requested
    timeFrom: Required[int]  # interval beginning (UNIX time)
    timeTo: Required[int]  # interval end (UNIX time)
    filter: str | None  # filter for search
    flags: int | None  # flags for loading messages
    flagsMask: int | None  # mask for flags
    loadCount: int | None  # how many messages to return


MessagesGetMessagesResponse = list[Message]  # list of messages


# messages/get_message_file
class MessagesGetMessageFileParams(TypedDict):
    itemId: int  # unit ID or resource ID
    fileId: str  # image file ID


# Response is an image, so we'll use `Union[bytes, None]` to represent the image data.
# If the request fails or there is no file, `None` can be used as the response.
MessagesGetMessageFileResponse = bytes | None


# messages/get_packed_messages
class MessagesGetPackedMessagesParams(TypedDict):
    itemId: int  # unit or resource ID
    timeFrom: int  # interval beginning (UNIX time)
    timeTo: int  # interval end (UNIX time)
    filtrationFlags: int  # optional, 0 or 1, default = 1 for message filtration by minimum satellites


class MessagesGetPackedMessagesResponse(TypedDict):
    messages: str  # encoded points (coordinates) by Google polyline


# messages/load_last
class MessagesLoadLastParams(TypedDict):
    itemId: int  # unit or resource ID
    lastTime: int  # time for which messages are requested (UNIX time)
    lastCount: int  # how many messages to load
    flags: int  # message flags: to load messages with defined flags only
    flagsMask: int  # mask (see Load messages for interval)
    loadCount: int  # how many messages to return


class MessagesLoadLastResponse(TypedDict):
    count: int  # number of messages
    messages: list[dict[str, Any]]  # array of messages


# messages/load_interval
class MessagesLoadIntervalParams(TypedDict):
    itemId: int  # unit or resource ID
    timeFrom: int  # interval beginning (UNIX time)
    timeTo: int  # interval end (UNIX time)
    flags: int  # flags for loading messages (see Data format: Messages)
    flagsMask: int  # mask for loading messages
    loadCount: int  # how many messages to return (0xffffffff - all found)


class MessagesLoadIntervalResponse(TypedDict):
    count: int  # number of messages
    messages: list[dict[str, Any]]  # array of messages
