# pylint: disable=missing-module-docstring,line-too-long,missing-class-docstring
from typing_extensions import TypedDict, Required, List


# unit_group/update_units
class UnitGroupUpdateUnitsParams(TypedDict):
    itemId: Required[int]
    units: Required[List[int]]


class UnitGroupUpdateUnitsResponse(TypedDict):
    u: List[int]
