"""Async lock for blocking async loop for long critical operations"""

import asyncio
from contextvars import ContextVar
from functools import wraps
from typing import Any


class ExclusiveAsyncLock:
    """
    Async lock for blocking async loop for long critical operations.
    Callers decorated with `lock` can still make requests without deadlocking —
    the context var tracks whether the current execution context holds the lock.
    """

    def __init__(self) -> None:
        self._lock: asyncio.Lock = asyncio.Lock()
        self._lock_event: asyncio.Event = asyncio.Event()
        self._lock_event.set()
        # per-instance ContextVar so multiple locks don't interfere
        self._in_lock: ContextVar[bool] = ContextVar(
            f"exclusive_lock_{id(self)}", default=False
        )

    def lock(self, func: Any = None) -> Any:
        """Decorator to lock async loop for long critical operations"""

        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            async with self._lock:
                self._lock_event.clear()
                token = self._in_lock.set(True)
                try:
                    return await func(*args, **kwargs)
                finally:
                    self._in_lock.reset(token)
                    self._lock_event.set()

        return wrapper

    async def wait(self) -> None:
        """Wait until the lock is released, unless the current context holds it"""

        if not self._in_lock.get() and self._lock.locked():
            await self._lock_event.wait()


__all__ = ("ExclusiveAsyncLock",)
