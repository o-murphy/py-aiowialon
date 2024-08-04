from dataclasses import dataclass, asdict
from typing import Optional, TypedDict
from strong_typing.serialization import json_to_object, object_to_json


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
