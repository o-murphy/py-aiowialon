


from pydantic import BaseModel, ConfigDict
from dataclasses import dataclass
from typing import TypedDict
from aiowialon.utils.compatibility import Unpack
from strong_typing.serialization import object_to_json
from aiowialon.types.flags import GetAccountResultType


class JsonRequestData2D(TypedDict, total=False):
    type: GetAccountResultType
    from_: int

@dataclass(kw_only=True)
class JsonRequestData2(BaseModel):
    model_config = ConfigDict(frozen=True)
    type: GetAccountResultType = GetAccountResultType.MINIMAL
    from_: int

    def __init__(self, /, **kwargs: Unpack[JsonRequestData2D]) -> None:
        super().__init__(**kwargs)

    def typed_dict(self) -> JsonRequestData2D:
        return JsonRequestData2D(**super().model_dump())

j = JsonRequestData2(from_=1)
print(j.model_dump())
print(object_to_json(j))
