"""
Some adjustments to allow using python <3.12
"""


try:
    from enum import StrEnum
except ImportError:
    try:
        from strenum import StrEnum
    except ImportError:
        from enum import Enum

        class StrEnum(str, Enum):
            pass

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack
