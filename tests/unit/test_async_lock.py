"""Tests for ExclusiveAsyncLock"""

import asyncio

import pytest

from aiowialon.utils.async_lock import ExclusiveAsyncLock


class TestExclusiveAsyncLock:
    async def test_wait_passes_when_not_locked(self):
        lock = ExclusiveAsyncLock()
        await lock.wait()  # should return immediately

    async def test_locked_context_can_call_wait_without_deadlock(self):
        lock = ExclusiveAsyncLock()
        entered = False

        @lock.lock
        async def critical():
            nonlocal entered
            entered = True
            await lock.wait()  # must not block

        await asyncio.wait_for(critical(), timeout=1.0)
        assert entered

    async def test_external_caller_waits_while_locked(self):
        lock = ExclusiveAsyncLock()
        order = []

        @lock.lock
        async def critical():
            order.append("in")
            await asyncio.sleep(0.05)
            order.append("out")

        async def outsider():
            await lock.wait()
            order.append("after")

        await asyncio.gather(critical(), outsider())
        assert order == ["in", "out", "after"]

    async def test_lock_releases_event_on_exit(self):
        lock = ExclusiveAsyncLock()

        @lock.lock
        async def critical():
            pass

        await critical()
        assert lock._lock_event.is_set()

    async def test_lock_releases_event_on_exception(self):
        lock = ExclusiveAsyncLock()

        @lock.lock
        async def critical():
            raise RuntimeError("boom")

        with pytest.raises(RuntimeError):
            await critical()

        assert lock._lock_event.is_set()
        assert not lock._lock.locked()

    async def test_two_instances_independent(self):
        lock1 = ExclusiveAsyncLock()
        lock2 = ExclusiveAsyncLock()

        waited = []

        @lock1.lock
        async def critical():
            # lock2.wait() must still block since we hold lock1, not lock2
            lock2._lock_event.clear()
            lock2._lock._locked = True  # simulate lock2 being held externally
            # context var for lock2 is NOT set → wait() would block
            assert not lock2._in_lock.get()

        await critical()
        assert not lock1._lock.locked()
