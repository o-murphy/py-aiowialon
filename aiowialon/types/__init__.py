"""
Types definition for aiowialon package.
We use these types to get specific behaviour of Wialon API client
and also for types annotations
"""

from .avl_events import *
from .login import *
from .multipart import *

# pylint: disable=duplicate-code
__all__ = (
    'LoginParams',
    'LoginCallback',
    'LogoutCallback',
    'flags',
    'AvlEvent',
    'AvlEventCallback',
    'AvlEventFilter',
    'AvlEventData',
    'AvlEventHandler',
    'MultipartField'
)
