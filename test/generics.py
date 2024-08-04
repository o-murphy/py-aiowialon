from dataclasses import dataclass
from functools import wraps
from typing import TypedDict, List, Optional, Union

from aiowialon.types.flags import AccessControlFlags, GetAccountResultType
from aiowialon.compatibility import Unpack
from strong_typing.serialization import json_to_object, object_to_json


# @warp
@dataclass(kw_only=True)
class JsonRequestData:
    class Params(TypedDict, total=False):
        # abstract Params(TypedDict)
        pass

    def __post_init__(self):
        # Initialize the instance using json_to_object if needed
        params = self.__dict__
        updated_instance = json_to_object(self.__class__, params)
        # Update the current instance's attributes
        self.__dict__.update(updated_instance.__dict__)

    def json(self):
        return object_to_json(self)

# @warp
@dataclass(kw_only=True)
class CoreGetAccountData(JsonRequestData):
    type: GetAccountResultType = GetAccountResultType.MINIMAL

    class Params(TypedDict, total=False):
        type: GetAccountResultType

# @warp
@dataclass(kw_only=True)
class CoreCheckItemsBilling(JsonRequestData):
    items: List[int]
    accessFlags: AccessControlFlags
    serviceName: str

    class Params(TypedDict, total=False):
        items: List[int]
        accessFlags: AccessControlFlags
        serviceName: str



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


def func(**kwargs: Unpack[CoreGetAccountData.Params]):
    obj = CoreGetAccountData(**kwargs)
    print(obj)
    json_data = obj.json()
    print(json_data)


func(type=2)
print(json_to_object(CoreGetAccountData, {}))
