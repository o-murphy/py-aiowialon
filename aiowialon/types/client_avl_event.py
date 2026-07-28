"""Object-oriented model for handled AVL-events"""

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any

import aiohttp

from aiowialon.exceptions import WialonError
from aiowialon.logger import logger
from aiowialon.types.api_types.other import AvlEventResponse, AvlEventType


@dataclass(frozen=True)
class AvlEventData:
    """Keeps AVL event data, qualified by item uid"""

    i: int
    t: AvlEventType
    d: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if isinstance(self.t, str):
            object.__setattr__(self, "t", AvlEventType(self.t))
        elif not isinstance(self.t, AvlEventType):
            raise TypeError(f"AvlEventData.t must be an instance of {AvlEventType}")


@dataclass(frozen=True)
class AvlEvent:
    """
    AVL event dataclass represents the Object-oriented AVL-event,
    used by AvlEventHandler
    """

    tm: int | None
    data: AvlEventData

    # pylint: disable=not-a-mapping
    def __post_init__(self):
        if not isinstance(self.data, AvlEventData):
            if isinstance(self.data, dict):
                object.__setattr__(self, "data", AvlEventData(**self.data))
            else:
                raise TypeError(f"AvlEvent.event has be a type of {AvlEventData}")

    @staticmethod
    def parse_avl_events_response(avl_events: AvlEventResponse) -> list["AvlEvent"]:
        """AVL-events response parser"""

        tm = avl_events.get("tm", None)
        events = avl_events.get("events", [])
        return [AvlEvent(tm, AvlEventData(**e)) for e in events]


AvlEventCallback = Callable[[AvlEvent], Awaitable[None]]
AvlEventFilter = Callable[[AvlEvent], bool]


class AvlEventHandler:
    """AvlEventHandler, using for handling AVL-events through registered callbacks"""

    def __init__(
        self, callback: AvlEventCallback, filter: AvlEventFilter | None = None
    ) -> None:
        self._callback: AvlEventCallback
        self._filter: AvlEventFilter | None
        self._queue: asyncio.Queue[AvlEvent] = asyncio.Queue()
        self._worker_task: asyncio.Task[None] | None = None

        self.callback = callback
        self.filter = filter

    def __call__(self, event: AvlEvent) -> bool:
        """
        Makes an AvlEventHandler instance callable,
        calls the callback function with handled AvlEvent instance
        returns True if filter was applied and callback enqueued
        and False otherwise
        """

        if self._filter is None or self._filter(event):
            self.__enqueue(event)
            return True
        return False

    def __enqueue(self, event: AvlEvent) -> None:
        logger.info("Got AVL event %s", event)
        self._queue.put_nowait(event)
        if self._worker_task is None or self._worker_task.done():
            self._worker_task = asyncio.create_task(
                self._run(),
                name=f"AvlEventHandler: {self._callback.__name__}",
            )

    async def _run(self) -> None:
        """Single worker that processes queued events sequentially"""

        while True:
            event = await self._queue.get()
            try:
                await self._callback(event)
            except asyncio.CancelledError:
                raise
            except (WialonError, aiohttp.ClientError):
                logger.exception(
                    "Exception happened in %s",
                    self._callback.__name__,
                )
            except Exception as e:  # noqa: BLE001
                logger.exception(
                    "Unknown exception happened in %s: %s",
                    self._callback.__name__,
                    e,
                )

    def cleanup(self) -> None:
        """Cancel the worker and drain the event queue"""

        logger.debug("Cleaning up AvlEventHandler: %s", self._callback.__name__)
        if self._worker_task and not self._worker_task.done():
            self._worker_task.cancel()
        while not self._queue.empty():
            self._queue.get_nowait()
        logger.debug("AvlEventHandler cleaned up")

    @property
    def callback(self) -> AvlEventCallback:
        """Returns current callback function"""

        return self._callback

    @callback.setter
    def callback(self, callback: AvlEventCallback) -> None:
        """Updates callback function with new one"""

        if not callable(callback):
            raise TypeError(
                f"AvlEventHandler.callback must be a type of {AvlEventCallback}"
            )
        self._callback = callback

    @property
    def filter(self) -> AvlEventFilter | None:
        """Returns current filter function"""

        return self._filter

    @filter.setter
    def filter(self, filter: AvlEventFilter | None = None) -> None:
        """Updates filter function with new one"""

        if filter is not None and not callable(filter):
            raise TypeError(
                f"AvlEventHandler.filter must be a type of {AvlEventFilter}"
            )
        self._filter = filter


__all__ = (
    "AvlEvent",
    "AvlEventCallback",
    "AvlEventData",
    "AvlEventFilter",
    "AvlEventHandler",
)
