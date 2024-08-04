from dataclasses import dataclass
from typing import TypedDict, List, Optional

from aiowialon.types.flags import AccessControlFlags, GetAccountResultType
from aiowialon.compatibility import Unpack
from strong_typing.serialization import json_to_object


@dataclass
class CoreGetAccountData:
    type: GetAccountResultType = GetAccountResultType.MINIMAL

    class Params(TypedDict, total=False):
        type: GetAccountResultType

    def __new__(cls, **kwargs: Unpack[Params]):
        return json_to_object(cls, kwargs)


@dataclass
class CoreCheckItemsBilling:
    items: List[int]
    accessFlags: AccessControlFlags
    serviceName: str

    class Params(TypedDict, total=False):
        items: List[int]
        accessFlags: AccessControlFlags
        serviceName: str

    def __new__(cls, **kwargs: Unpack[Params]):
        return json_to_object(cls, kwargs)


@dataclass
class TSearchSpec:
    itemsType: str
    propName: str
    propValueMask: str
    sortType: str
    propType: Optional[str]
    or_logic: Optional[bool] = False


@dataclass
class TSearchAction:
    spec: TSearchSpec
    force: int = 0
    flags: int = 0
    from_: int = 0
    to: int = 0


class SearchRequest(TypedDict):
    action: TSearchAction
