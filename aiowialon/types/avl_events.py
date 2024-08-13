"""Object-oriented model for handled AVL-events"""

import asyncio
from contextlib import suppress
from dataclasses import dataclass, field
from typing import Optional, Callable, Coroutine, Dict, Any, List, Union

import aiohttp

from aiowialon.exceptions import WialonError
from aiowialon.logger import logger
from aiowialon.utils.compat import StrEnum


class AvlEventType(StrEnum):
    """AVL event types"""

    MESSAGE = "m"
    UPDATE = "u"
    DELETE = "d"


@dataclass(frozen=True)
class AvlEventData:
    """Keeps AVL event data, qualified by item uid"""

    i: int
    t: AvlEventType
    d: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.t, AvlEventType) and isinstance(self.t, str):
            object.__setattr__(self, 't', AvlEventType(self.t))
        else:
            raise TypeError(f"AvlEventData.t has be a type of {AvlEventType}")


@dataclass(frozen=True)
class AvlEvent:
    """
    AVL event dataclass represents the Object-oriented AVL-event,
    used by AvlEventHandler
    """

    tm: Union[int, None]
    data: AvlEventData

    # pylint: disable=not-a-mapping
    def __post_init__(self):
        if not isinstance(self.data, AvlEventData):
            if isinstance(self.data, dict):
                object.__setattr__(self, 'data', AvlEventData(**self.data))
            else:
                raise TypeError(f"AvlEvent.event has be a type of {AvlEventData}")

    @staticmethod
    def parse_avl_events_response(avl_events: Dict[str, Any]) -> List['AvlEvent']:
        """AVL-events response parser"""

        tm = avl_events.get('tm', None)
        events = avl_events.get('events', [])
        return [AvlEvent(tm, e) for e in events]


AvlEventCallback = Callable[[AvlEvent], Coroutine]
AvlEventFilter = Callable[[AvlEvent], bool]


class AvlEventHandler:
    """AvlEventHandler, using for handling AVL-events through registered callbacks"""

    def __init__(self,
                 callback: AvlEventCallback,
                 filter_: Optional[AvlEventFilter] = None) -> None:
        self._callback: AvlEventCallback
        self._filter: Optional[AvlEventFilter]
        self._tasks: List[asyncio.Task] = []

        self.callback = callback
        self.filter = filter_

    async def __call__(self, event: AvlEvent) -> bool:
        """
        Makes an AvlEventHandler instance callable,
        calls the callback function with handled AvlEvent instance
        returns True if filter was applied and callback task executed
        and False otherwise
        """

        if not self._filter:
            await self.__process_event(event)
            return True
        if self._filter is not None:
            if self._filter(event):
                await self.__process_event(event)
                return True
        return False

    async def __process_event(self, event: AvlEvent) -> None:
        """
        Executes the callback function with handled AvlEvent,
        suppressing the exceptions if callback raises it to prevent app breaking.
        """

        logger.info("Got AVL event %s", event)
        with suppress(asyncio.CancelledError):
            # Wrap the callback with a try-except block to handle exceptions
            async def wrapped_callback(event: AvlEvent):
                try:
                    await self._callback(event)
                except (WialonError, aiohttp.ClientError) as e:
                    logger.error("Exception happened in %s", self._callback.__name__)
                    logger.exception(e)

            callback_task = asyncio.create_task(
                wrapped_callback(event),
                name=f"AvlEventHandler ({len(self._tasks)}): {self._callback.__name__}"
            )
            self._tasks.append(callback_task)
            callback_task.add_done_callback(self.__cleanup_task)

    def __cleanup_task(self, task: asyncio.Task):
        """Remove the task from the list once it's done"""

        task.cancel()
        with suppress(asyncio.CancelledError):
            task.__await__()
        if task in self._tasks:
            self._tasks.remove(task)
        logger.debug("Task completed and removed: %s", task.get_name())

    def cleanup(self):
        """cleaning the AvlEventHandler tasks"""

        logger.debug("Cleaning up AvlEventHandler: %s, cancelling all tasks",
                     self._callback.__name__)
        for task in self._tasks:
            self.__cleanup_task(task)
        logger.debug("All handler tasks cancelled")

    @property
    def callback(self) -> AvlEventCallback:
        """Returns current callback function"""

        return self._callback

    @callback.setter
    def callback(self, callback: AvlEventCallback) -> None:
        """Updates callback function with new one"""

        if not callable(callback):
            raise TypeError(
                f'AvlEventHandler.callback must be a type of {AvlEventCallback}'
            )
        self._callback = callback

    @property
    def filter(self) -> Optional[AvlEventFilter]:
        """Returns current filter function"""

        return self._filter

    @filter.setter
    def filter(self, filter_: Optional[AvlEventFilter] = None) -> None:
        """Updates filter function with new one"""

        if filter_ and not callable(filter_):
            raise TypeError(f'AvlEventHandler.filter_ must be a type of {AvlEventFilter}')
        self._filter = filter_


__all__ = (
    'AvlEvent',
    'AvlEventCallback',
    'AvlEventFilter',
    'AvlEventData',
    'AvlEventHandler',
)
