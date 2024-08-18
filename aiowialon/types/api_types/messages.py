# pylint: disable=missing-module-docstring,line-too-long,missing-class-docstring
from enum import IntEnum
from typing_extensions import TypedDict, Required, Optional, Any, Dict, List, Union

Incomplete = Any

# messages/unload
MessagesUnloadResponse = Dict[str, Any]


# messages/delete_message
class MessagesDeleteMessageParams(TypedDict):
    msgIndex: Required[int]  # message index


class MessagesDeleteMessageResponse(TypedDict):
    pass  # empty object if execution is successful


class MessagesDeleteMessageErrorCodes(IntEnum):
    NO_SUCH_MESSAGE_OR_CANNOT_DELETE_LAST = 4  # No such message or this message is the last one and cannot be deleted
    ERROR_DELETING_MESSAGE = 6  # Error deleting message


# messages/get_messages
class Position(TypedDict):
    y: Optional[float]
    x: Optional[float]
    z: Optional[float]
    s: Optional[int]
    c: Optional[int]
    sc: Optional[int]


class Parameters(TypedDict):
    adc1: Optional[int]
    pre2: Optional[int]
    param: Optional[int]
    param5: Optional[int]


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
    filter: Optional[str]  # filter for search
    flags: Optional[int]  # flags for loading messages
    flagsMask: Optional[int]  # mask for flags
    loadCount: Optional[int]  # how many messages to return


MessagesGetMessagesResponse = List[Message]  # list of messages


# messages/get_message_file
class MessagesGetMessageFileParams(TypedDict):
    itemId: int  # unit ID or resource ID
    fileId: str  # image file ID


# Response is an image, so we'll use `Union[bytes, None]` to represent the image data.
# If the request fails or there is no file, `None` can be used as the response.
MessagesGetMessageFileResponse = Union[bytes, None]


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
    messages: List[Dict[str, Any]]  # array of messages


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
    messages: List[Dict[str, Any]]  # array of messages
