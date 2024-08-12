"""
Compatibility module to allow using python <3.12
"""

# pylint: skip-file,disable-all


import sys

if sys.version_info[:2] < (3, 11):
    from typing_extensions import Unpack
    from strenum import StrEnum
else:
    from typing import Unpack
    from enum import StrEnum

__all__ = (
    'StrEnum',
    'Unpack'
)
