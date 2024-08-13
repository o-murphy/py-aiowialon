"""Async lock for blocking async loop for long critical operations"""

import asyncio
import inspect
from functools import wraps
from typing import Optional, Any


class ExclusiveAsyncLock:
    """
    Async lock for blocking async loop for long critical operations
    for exclusive access
    """

    def __init__(self) -> None:
        self._lock: asyncio.Lock = asyncio.Lock()
        self._lock_event: asyncio.Event = asyncio.Event()
        self._lock_event.set()
        self._exclusive_frame: Optional[inspect.FrameInfo] = None

    def lock(self, func=None) -> Any:
        """Decorator to lock async loop for long critical operations"""

        @wraps(func)
        async def wrapper(*args, **kwargs):
            async with self._lock:
                self._lock_event.clear()
                try:
                    coroutine = func(*args, **kwargs)
                    self._exclusive_frame = coroutine.cr_frame
                    return await coroutine
                finally:
                    self._exclusive_frame = None
                    self._lock_event.set()

        return wrapper

    async def wait(self) -> None:
        """waits until lock release"""

        if self._lock.locked() and self._exclusive_frame:
            current_frame = inspect.currentframe()
            while current_frame is not None:
                if current_frame is self._exclusive_frame:
                    return
                current_frame = current_frame.f_back
            await self._lock_event.wait()


__all__ = ['ExclusiveAsyncLock']
