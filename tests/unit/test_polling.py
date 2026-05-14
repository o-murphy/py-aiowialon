"""Tests for Wialon polling loop and event dispatch"""

import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from aiowialon.api import Wialon
from aiowialon.types.client_avl_event import AvlEvent, AvlEventData
from aiowialon.types.api_types.other import AvlEventType
from aiowialon.exceptions import WialonRequestLimitExceededError


def make_avl_response(events=None, tm=0):
    return {"tm": tm, "events": events or []}


def make_raw_event(i=1, t="m", d=None):
    return {"i": i, "t": t, "d": d or {}}


@pytest.fixture
async def wialon():
    w = Wialon(token="test-token")
    w._sid = "fake-sid"
    yield w
    w._cleanup_event_handlers()
    await asyncio.sleep(0.05)


class TestProcessEventHandlers:
    def test_no_handlers_no_error(self, wialon):
        event = AvlEvent(tm=0, data=AvlEventData(i=1, t=AvlEventType.MESSAGE))
        wialon._process_event_handlers(event)

    async def test_handler_called_when_no_filter(self, wialon):
        received = []

        async def cb(event):
            received.append(event)

        wialon.avl_event_handler()(cb)
        event = AvlEvent(tm=0, data=AvlEventData(i=1, t=AvlEventType.MESSAGE))
        wialon._process_event_handlers(event)
        await asyncio.sleep(0.05)
        assert len(received) == 1

    async def test_handler_stops_at_first_match(self, wialon):
        received = []

        async def cb1(event):
            received.append("cb1")

        async def cb2(event):
            received.append("cb2")

        wialon.avl_event_handler()(cb1)
        wialon.avl_event_handler()(cb2)

        event = AvlEvent(tm=0, data=AvlEventData(i=1, t=AvlEventType.MESSAGE))
        wialon._process_event_handlers(event)
        await asyncio.sleep(0.05)
        # cb1 matched (no filter) → break → cb2 not enqueued
        assert received == ["cb1"]

    async def test_filter_skips_handler_to_next(self, wialon):
        received = []

        async def cb1(event):
            received.append("cb1")

        async def cb2(event):
            received.append("cb2")

        wialon.avl_event_handler(filter=lambda e: e.data.i == 99)(cb1)
        wialon.avl_event_handler()(cb2)

        event = AvlEvent(tm=0, data=AvlEventData(i=1, t=AvlEventType.MESSAGE))
        wialon._process_event_handlers(event)
        await asyncio.sleep(0.05)
        # cb1 filter=99 doesn't match i=1 → cb2 (no filter) matches
        assert received == ["cb2"]


class TestPollingLoop:
    @pytest.mark.asyncio
    async def test_polling_calls_avl_evts_and_dispatches(self, wialon):
        received = []

        async def cb(event):
            received.append(event)

        wialon.avl_event_handler()(cb)

        call_count = 0

        async def fake_avl_evts():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return make_avl_response([make_raw_event(i=42)])
            wialon._sid = None  # stop loop after 2nd iteration
            return make_avl_response()

        with patch.object(wialon, "avl_evts", side_effect=fake_avl_evts):
            await wialon._polling(timeout=0)

        await asyncio.sleep(0.1)
        assert len(received) == 1
        assert received[0].data.i == 42

    @pytest.mark.asyncio
    async def test_polling_handles_request_limit_error(self, wialon):
        call_count = 0

        async def fake_avl_evts():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise WialonRequestLimitExceededError()
            wialon._sid = None
            return make_avl_response()

        with patch.object(wialon, "avl_evts", side_effect=fake_avl_evts):
            await wialon._polling(timeout=0)

        assert call_count == 2  # continued after the error

    @pytest.mark.asyncio
    async def test_polling_stops_when_sid_cleared(self, wialon):
        call_count = 0

        async def fake_avl_evts():
            nonlocal call_count
            call_count += 1
            wialon._sid = None
            return make_avl_response()

        with patch.object(wialon, "avl_evts", side_effect=fake_avl_evts):
            await wialon._polling(timeout=0)

        assert call_count == 1


class TestAvlEventHandlerRegistration:
    def test_register_handler(self, wialon):
        async def cb(event): pass
        wialon.avl_event_handler()(cb)
        assert "cb" in wialon._Wialon__avl_event_handlers

    def test_duplicate_handler_raises(self, wialon):
        async def cb(event): pass
        wialon.avl_event_handler()(cb)
        with pytest.raises(KeyError):
            wialon.avl_event_handler()(cb)

    def test_remove_handler(self, wialon):
        async def cb(event): pass
        wialon.avl_event_handler()(cb)
        wialon.remove_avl_event_handler(cb)
        assert "cb" not in wialon._Wialon__avl_event_handlers

    def test_remove_handler_by_name(self, wialon):
        async def cb(event): pass
        wialon.avl_event_handler()(cb)
        wialon.remove_avl_event_handler("cb")
        assert "cb" not in wialon._Wialon__avl_event_handlers

    @pytest.mark.asyncio
    async def test_avl_event_once_removes_after_call(self, wialon):
        calls = []

        async def cb(event):
            calls.append(event)

        cb = wialon.avl_event_once(cb)
        wialon.avl_event_handler()(cb)

        event = AvlEvent(tm=0, data=AvlEventData(i=1, t=AvlEventType.MESSAGE))
        wialon._process_event_handlers(event)
        await asyncio.sleep(0.1)

        assert "cb" not in wialon._Wialon__avl_event_handlers


class TestCleanupEventHandlers:
    def test_cleanup_cancels_all_handlers(self, wialon):
        async def cb1(event): pass
        async def cb2(event): pass

        wialon.avl_event_handler()(cb1)
        wialon.avl_event_handler()(cb2)

        wialon._cleanup_event_handlers()
        for handler in wialon._Wialon__avl_event_handlers.values():
            assert handler._queue.empty()
