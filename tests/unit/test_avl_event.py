"""Tests for AvlEventData, AvlEvent, AvlEventHandler"""

import asyncio

import pytest

from aiowialon.types.client_avl_event import (
    AvlEvent,
    AvlEventData,
    AvlEventHandler,
)
from aiowialon.types.api_types.other import AvlEventType
from aiowialon.exceptions import WialonError


# ---------------------------------------------------------------------------
# AvlEventData
# ---------------------------------------------------------------------------

class TestAvlEventData:
    def test_create_with_enum(self):
        d = AvlEventData(i=1, t=AvlEventType.MESSAGE)
        assert d.i == 1
        assert d.t is AvlEventType.MESSAGE

    def test_create_with_string_coerced_to_enum(self):
        d = AvlEventData(i=1, t="m")
        assert d.t is AvlEventType.MESSAGE

    def test_invalid_type_raises(self):
        with pytest.raises(TypeError):
            AvlEventData(i=1, t=999)

    def test_frozen(self):
        d = AvlEventData(i=1, t=AvlEventType.MESSAGE)
        with pytest.raises((AttributeError, TypeError)):
            d.i = 2

    def test_default_d_is_empty_dict(self):
        d = AvlEventData(i=1, t=AvlEventType.UPDATE)
        assert d.d == {}

    def test_d_not_shared_between_instances(self):
        d1 = AvlEventData(i=1, t=AvlEventType.MESSAGE)
        d2 = AvlEventData(i=2, t=AvlEventType.MESSAGE)
        assert d1.d is not d2.d


# ---------------------------------------------------------------------------
# AvlEvent
# ---------------------------------------------------------------------------

class TestAvlEvent:
    def test_create_with_avl_event_data(self):
        data = AvlEventData(i=42, t=AvlEventType.MESSAGE)
        event = AvlEvent(tm=1000, data=data)
        assert event.tm == 1000
        assert event.data is data

    def test_create_with_dict_coerced(self):
        event = AvlEvent(tm=0, data={"i": 1, "t": "m"})
        assert isinstance(event.data, AvlEventData)
        assert event.data.i == 1

    def test_invalid_data_type_raises(self):
        with pytest.raises(TypeError):
            AvlEvent(tm=0, data="bad")

    def test_tm_can_be_none(self):
        event = AvlEvent(tm=None, data=AvlEventData(i=1, t=AvlEventType.DELETE))
        assert event.tm is None

    def test_parse_avl_events_response_empty(self):
        result = AvlEvent.parse_avl_events_response({"tm": 100, "events": []})
        assert result == []

    def test_parse_avl_events_response_single(self):
        response = {"tm": 500, "events": [{"i": 7, "t": "u", "d": {}}]}
        events = AvlEvent.parse_avl_events_response(response)
        assert len(events) == 1
        assert events[0].tm == 500
        assert events[0].data.i == 7
        assert events[0].data.t is AvlEventType.UPDATE

    def test_parse_avl_events_response_multiple(self):
        response = {
            "tm": 1,
            "events": [
                {"i": 1, "t": "m", "d": {}},
                {"i": 2, "t": "d", "d": {"x": 1}},
            ],
        }
        events = AvlEvent.parse_avl_events_response(response)
        assert len(events) == 2
        assert events[1].data.d == {"x": 1}

    def test_parse_missing_events_key(self):
        result = AvlEvent.parse_avl_events_response({"tm": 0})
        assert result == []

    def test_parse_missing_tm_key(self):
        response = {"events": [{"i": 1, "t": "m", "d": {}}]}
        events = AvlEvent.parse_avl_events_response(response)
        assert events[0].tm is None


# ---------------------------------------------------------------------------
# AvlEventHandler — filter & queue (need running event loop)
# ---------------------------------------------------------------------------

def make_event(i: int = 1) -> AvlEvent:
    return AvlEvent(tm=0, data=AvlEventData(i=i, t=AvlEventType.MESSAGE))


class TestAvlEventHandlerFilter:
    async def test_no_filter_always_returns_true(self):
        async def cb(e): pass
        handler = AvlEventHandler(callback=cb)
        assert handler(make_event()) is True
        handler.cleanup()

    async def test_filter_match_returns_true(self):
        async def cb(e): pass
        handler = AvlEventHandler(callback=cb, filter=lambda e: e.data.i == 1)
        assert handler(make_event(i=1)) is True
        handler.cleanup()

    def test_filter_no_match_returns_false(self):
        async def cb(e): pass
        # filter mismatch never reaches create_task, safe to call sync
        handler = AvlEventHandler(callback=cb, filter=lambda e: e.data.i == 99)
        assert handler(make_event(i=1)) is False

    def test_invalid_callback_raises(self):
        with pytest.raises(TypeError):
            AvlEventHandler(callback="not_callable")

    def test_invalid_filter_raises(self):
        async def cb(e): pass
        with pytest.raises(TypeError):
            AvlEventHandler(callback=cb, filter="not_callable")


class TestAvlEventHandlerQueue:
    async def test_callback_called_with_event(self):
        received = []

        async def cb(event):
            received.append(event)

        handler = AvlEventHandler(callback=cb)
        event = make_event()
        handler(event)
        await asyncio.sleep(0.05)
        assert received == [event]
        handler.cleanup()

    async def test_multiple_events_processed_in_order(self):
        received = []

        async def cb(event):
            received.append(event.data.i)

        handler = AvlEventHandler(callback=cb)
        for i in range(5):
            handler(make_event(i=i))

        await asyncio.sleep(0.1)
        assert received == list(range(5))
        handler.cleanup()

    async def test_single_worker_task_reused(self):
        async def cb(event):
            await asyncio.sleep(0)

        handler = AvlEventHandler(callback=cb)
        handler(make_event())
        task1 = handler._worker_task
        handler(make_event())
        task2 = handler._worker_task
        assert task1 is task2
        await asyncio.sleep(0.05)
        handler.cleanup()

    async def test_exception_in_callback_does_not_stop_worker(self):
        received = []

        async def cb(event):
            if event.data.i == 0:
                raise RuntimeError("boom")
            received.append(event.data.i)

        handler = AvlEventHandler(callback=cb)
        handler(make_event(i=0))
        handler(make_event(i=1))
        await asyncio.sleep(0.1)
        assert 1 in received
        handler.cleanup()

    async def test_wialon_error_in_callback_does_not_stop_worker(self):
        received = []

        async def cb(event):
            if event.data.i == 0:
                raise WialonError(5)
            received.append(event.data.i)

        handler = AvlEventHandler(callback=cb)
        handler(make_event(i=0))
        handler(make_event(i=1))
        await asyncio.sleep(0.1)
        assert 1 in received
        handler.cleanup()

    async def test_cleanup_cancels_worker(self):
        async def cb(event):
            await asyncio.sleep(10)

        handler = AvlEventHandler(callback=cb)
        handler(make_event())
        await asyncio.sleep(0.05)
        assert handler._worker_task and not handler._worker_task.done()

        handler.cleanup()
        await asyncio.sleep(0.05)
        assert handler._worker_task.done()

    async def test_cleanup_drains_queue(self):
        processing = asyncio.Event()

        async def cb(event):
            processing.set()
            await asyncio.sleep(10)

        handler = AvlEventHandler(callback=cb)
        handler(make_event(i=0))
        handler(make_event(i=1))
        handler(make_event(i=2))

        await processing.wait()
        handler.cleanup()
        assert handler._queue.empty()

    async def test_filter_prevents_enqueue(self):
        received = []

        async def cb(event):
            received.append(event)

        handler = AvlEventHandler(callback=cb, filter=lambda e: e.data.i == 99)
        handler(make_event(i=1))
        await asyncio.sleep(0.05)
        assert received == []
        assert handler._worker_task is None


class TestAvlEventHandlerProperties:
    def test_callback_property_get(self):
        async def cb(e): pass
        handler = AvlEventHandler(callback=cb)
        assert handler.callback is cb

    def test_callback_property_set(self):
        async def cb1(e): pass
        async def cb2(e): pass
        handler = AvlEventHandler(callback=cb1)
        handler.callback = cb2
        assert handler.callback is cb2

    def test_filter_property_none_by_default(self):
        async def cb(e): pass
        handler = AvlEventHandler(callback=cb)
        assert handler.filter is None

    def test_filter_property_set(self):
        async def cb(e): pass
        f = lambda e: True
        handler = AvlEventHandler(callback=cb)
        handler.filter = f
        assert handler.filter is f

    def test_filter_property_set_none(self):
        async def cb(e): pass
        handler = AvlEventHandler(callback=cb, filter=lambda e: True)
        handler.filter = None
        assert handler.filter is None
