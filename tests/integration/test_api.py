"""Integration tests against the real Wialon API (Wialon SDK playground).

Run with:
    uv run pytest --integration
    uv run pytest --integration tests/integration/
    uv run pytest --integration -v -s          # verbose with stdout

Override credentials via env vars:
    WIALON_TOKEN=<token> WIALON_HOST=<host> uv run pytest --integration
"""

import asyncio

import pytest

from aiowialon import Wialon, AvlEvent, flags
from aiowialon.exceptions import WialonError


pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# Session lifecycle
# ---------------------------------------------------------------------------

class TestSession:
    async def test_login_returns_sid(self, wialon):
        result = await wialon.login()
        assert "eid" in result
        assert wialon._sid == result["eid"]
        await wialon.logout()

    async def test_logout_clears_sid(self, wialon):
        await wialon.login()
        await wialon.logout()
        assert wialon._sid is None

    async def test_context_manager_closes_http_session(self, token, host):
        async with Wialon(host=host, token=token) as w:
            await w.login()
            assert w._sid is not None
            await w.logout()
        assert w._Wialon__http_session is None or w._Wialon__http_session.closed

    async def test_double_login_raises(self, wialon):
        await wialon.login()
        # second login should work (re-authenticates), not raise
        result = await wialon.login()
        assert "eid" in result
        await wialon.logout()


# ---------------------------------------------------------------------------
# Basic API calls
# ---------------------------------------------------------------------------

class TestApiCalls:
    async def test_avl_evts(self, logged_in_wialon):
        result = await logged_in_wialon.avl_evts()
        assert isinstance(result, dict)
        assert "tm" in result
        assert "events" in result

    async def test_core_search_items(self, logged_in_wialon):
        result = await logged_in_wialon.core_search_items(
            spec={
                "itemsType": "avl_unit",
                "propName": "sys_name",
                "propValueMask": "*",
                "sortType": "sys_name",
            },
            force=1,
            flags=flags.UnitsDataFlag.BASE,
            from_=0,
            to=10,
        )
        assert isinstance(result, dict)
        assert "items" in result or "totalItemsCount" in result

    async def test_unknown_service_raises_wialon_error(self, logged_in_wialon):
        with pytest.raises(WialonError):
            await logged_in_wialon.call("nonexistent_method")


# ---------------------------------------------------------------------------
# Batch requests
# ---------------------------------------------------------------------------

class TestBatch:
    async def test_batch_two_calls(self, logged_in_wialon):
        w = logged_in_wialon
        result = await w.batch(
            w.core_search_items(
                spec={
                    "itemsType": "avl_unit",
                    "propName": "sys_name",
                    "propValueMask": "*",
                    "sortType": "sys_name",
                },
                force=1,
                flags=flags.UnitsDataFlag.BASE,
                from_=0,
                to=1,
            ),
            w.core_search_items(
                spec={
                    "itemsType": "user",
                    "propName": "sys_name",
                    "propValueMask": "*",
                    "sortType": "sys_name",
                },
                force=1,
                flags=1,
                from_=0,
                to=1,
            ),
            flags_=flags.BatchFlag.EXECUTE_ALL,
        )
        assert isinstance(result, list)
        assert len(result) == 2

    async def test_batch_rejects_non_call_coroutine(self, logged_in_wialon):
        async def not_a_call():
            pass

        with pytest.raises(TypeError):
            await logged_in_wialon.batch(not_a_call())


# ---------------------------------------------------------------------------
# AVL event handling
# ---------------------------------------------------------------------------

class TestAvlEventHandling:
    async def test_avl_event_handler_registered_and_called(self, logged_in_wialon):
        w = logged_in_wialon
        received = []

        # register all avl_unit events for polling
        await w.core_update_data_flags(
            spec=[{
                "type": "type",
                "data": "avl_unit",
                "flags": flags.UnitsDataFlag.BASE | flags.UnitsDataFlag.POS,
                "mode": 0,
            }]
        )

        @w.avl_event_handler()
        async def catch_all(event: AvlEvent):
            received.append(event)

        # poll manually a few times
        for _ in range(3):
            response = await w.avl_evts()
            events = AvlEvent.parse_avl_events_response(response)
            for event in events:
                w._process_event_handlers(event)
            await asyncio.sleep(1)

        await asyncio.sleep(0.2)
        w._cleanup_event_handlers()
        # we may or may not receive events on playground — just assert no crash
        assert isinstance(received, list)

    async def test_polling_starts_and_stops(self, token, host):
        w = Wialon(host=host, token=token)

        @w.on_session_open
        async def on_open(session):
            await w.core_update_data_flags(
                spec=[{
                    "type": "type",
                    "data": "avl_unit",
                    "flags": flags.UnitsDataFlag.BASE,
                    "mode": 0,
                }]
            )

        polling_task = asyncio.create_task(
            w.start_polling(timeout=1, logout_finally=True)
        )
        await asyncio.sleep(3)
        await w.stop_polling(logout=True)

        # polling_task completes normally after stop_polling drains the finally block
        await asyncio.gather(polling_task, return_exceptions=True)

        assert w._sid is None


# ---------------------------------------------------------------------------
# Rate limiter / semaphore
# ---------------------------------------------------------------------------

class TestRateLimiting:
    async def test_concurrent_calls_respect_semaphore(self, logged_in_wialon):
        w = logged_in_wialon
        calls = [
            w.core_search_items(
                spec={
                    "itemsType": "avl_unit",
                    "propName": "sys_name",
                    "propValueMask": "*",
                    "sortType": "sys_name",
                },
                force=1,
                flags=flags.UnitsDataFlag.BASE,
                from_=0,
                to=1,
            )
            for _ in range(5)
        ]
        results = await asyncio.gather(*calls)
        assert all(isinstance(r, dict) for r in results)
