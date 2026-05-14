import inspect
from dataclasses import dataclass
from typing import TypedDict, List, Optional

from aiowialon.types.flags import AccessControlFlags, GetAccountResultType
from aiowialon.utils.compatibility import Unpack
from strong_typing.serialization import json_to_object, object_to_json
from abc import ABC


@dataclass(kw_only=True)
class JsonRequestData(ABC):
    class Params(TypedDict, total=False):
        # abstract Params(TypedDict)
        pass

    def __init__(self, **kwargs: Unpack[Params]):
        super().__init__(self, **kwargs)

    def __post_init__(self):
        # Initialize the instance using json_to_object if needed
        updated_instance = json_to_object(self.__class__, self.__dict__)
        # Update the current instance's attributes
        self.__dict__.update(updated_instance.__dict__)

    def json(self):
        return object_to_json(self)


@dataclass(kw_only=True)
class CoreGetAccountData(JsonRequestData):
    type: GetAccountResultType = GetAccountResultType.MINIMAL

    class Params(TypedDict, total=False):
        type: GetAccountResultType


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


def print_classes_in_scope():
    # Get the current module
    current_module = inspect.getmodule(inspect.currentframe())
    # Iterate over all items in the module's dictionary
    for name, obj in current_module.__dict__.items():
        # Check if the object is a class
        if inspect.isclass(obj):
            print(name)


print_classes_in_scope()
