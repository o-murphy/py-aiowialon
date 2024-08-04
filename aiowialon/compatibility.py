"""
Some adjustments to allow using python 3.9+
"""

try:
    from enum import StrEnum
except ImportError:
    from strenum import StrEnum

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack
