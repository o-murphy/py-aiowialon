# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0b2] - 2026-07-13

### Removed
- Dropped support of python 3.8 and python 3.9

### Changed
- Updated annotations to match python 3.10 annotations syntax

## [2.0.0b1] - 2026-05-14

> Major library overhaul: queue-based AVL event dispatch, persistent HTTP session, full test suite, and PEP 561 typing support.

### Upgrade Notes

- Rename `avl_event_handler(filter_=...)` → `filter=` in all handler registrations.
- Rename `ClientLoginParams` key `hash` → `auth_hash` if you pass it explicitly.
- Remove `await` from any direct calls to `_process_event_handlers()` and
  `_cleanup_event_handlers()` — both are now regular functions.
- If you subclassed or called `AvlEventHandler.__call__()` directly, remove `await` — it
  is now synchronous and enqueues the event instead of dispatching immediately.
- Unknown Wialon error codes now raise `WialonError` instead of being silently ignored.
  Review any bare `except` blocks around `Wialon.call()`.

### Added

- `Wialon` is now an async context manager — `async with Wialon(...) as w:` closes the HTTP
  session automatically on exit.
- Persistent `aiohttp.ClientSession` — one session is created lazily on the first request and
  reused for the entire login lifecycle, then closed on `logout()`. Avoids repeated TLS
  handshakes and connector overhead.
- `logout()` is safe against concurrent calls — a lock prevents a race where both
  `stop_polling(logout=True)` and `logout_finally=True` try to close the session simultaneously.
- `py.typed` marker (PEP 561) — downstream packages and type checkers now pick up the bundled
  type stubs automatically.
- Explicit `__all__` in `aiowialon/__init__.py` — public API surface is now clearly defined;
  internal symbols are no longer re-exported via wildcard imports.
- Unit test suite: 110 tests across `test_avl_event`, `test_async_lock`, `test_convention`,
  `test_exceptions`, `test_validators`, and `test_polling`.
- Integration tests against the Wialon playground — run with `pytest --integration`. Skipped
  by default. Credentials can be overridden with `WIALON_TOKEN` / `WIALON_HOST` env vars.
- CI: `test.yml` exposes a `workflow_call` trigger; called as a required gate by `release.yml`
  before any PyPI publish.
- CI: `release.yml` — unified release workflow: runs tests, generates release notes from
  `CHANGELOG.md`, creates a draft GitHub Release, builds wheel + sdist, publishes to PyPI or
  TestPyPI, then undrafts the release. Supports `workflow_dispatch` with TestPyPI and version
  override inputs.
- CI: `.github/actions/gen_release_notes` — reusable composite action that parses
  `CHANGELOG.md` and renders formatted GitHub release notes (intro, highlights, upgrade notes,
  contributors, comparison link).
- CI job step summaries — each matrix leg writes a per-Python-version test report and security
  audit table directly to the GitHub Actions summary page.

### Changed

- **BREAKING** — `avl_event_handler(filter_=...)` keyword argument renamed to `filter=`.
- **BREAKING** — `ClientLoginParams` field `hash` renamed to `auth_hash` to avoid shadowing
  the Python builtin.
- **BREAKING** — AVL event dispatch replaced: the old unbounded `asyncio.create_task` fan-out
  (one task per event per handler) is replaced by an `asyncio.Queue` + single persistent worker
  task per handler. Backpressure is now bounded; events are processed in order.
- **BREAKING** — `AvlEventHandler.__call__` is now a regular `def`, not `async def`. Callers
  must not `await` it. The method enqueues the event and returns a `bool`.
- **BREAKING** — `Wialon._process_event_handlers` is now a regular `def`. Direct callers must
  remove `await`.
- **BREAKING** — `Wialon._cleanup_event_handlers` is now a regular `def`. Direct callers must
  remove `await`.
- `ExclusiveAsyncLock` reimplemented with `contextvars.ContextVar` instead of CPython frame
  stack inspection — portable across Python implementations and async frameworks.
- `AvlEventCallback` type alias updated from `Callable[[AvlEvent], Coroutine]` to
  `Callable[[AvlEvent], Awaitable[None]]` — more accurate and compatible with `asyncio.coroutine`
  deprecation.
- `ClientLoginCallback` and `ClientLogoutCallback` updated from `Coroutine` to
  `Awaitable[None]` for the same reason.

### Fixed

- Validator silently discarded Wialon error responses whose code was not in the known error
  table — they are now always raised as `WialonError`.
- `WialonError.__str__` returned an empty string for unknown error codes — now falls back to
  the description for code 6 ("Unknown error").
- `_process_event_handlers` was declared `async` but its return value was never awaited inside
  `_polling`, causing a `RuntimeWarning: coroutine was never awaited`.
- Leftover `print(coroutine)` debug statement in `batch()` removed.
- `examples/direct.py`: removed assignment to non-existent attribute `wialon.sid`.
- `examples/polling.py`: removed dead `asyncio.Event().clear()` call.
- `WialonError.errors` dict lookup now uses `.get()` with a safe fallback instead of bare
  key access that could raise `KeyError` on unknown codes.

### Removed

- `AvlEventHandler._tasks: List[asyncio.Task]` — superseded by the queue-based worker.
- `from aiowialon.X import *` wildcard re-exports from `__init__.py` — replaced by an
  explicit import list. Any private symbols that leaked via wildcards are no longer public.

## [1.3.5] - 2025-06-25

### Changed

- `prepare_action_name` convention updated for edge-case service names.
- CI: restored GitHub Actions workflows after repository migration.

## [1.3.4.post1] - 2025-05-28

### Changed

- CI workflow fixes (publish, test pipelines).

## [1.3.3] - 2024-08-17

### Added

- `Wialon.wait()` — decorator that overrides the request timeout for a single call.

## [1.3.2] - 2024-08-13

### Added

- `Wialon.session_lock` — `ExclusiveAsyncLock` decorator for long critical operations inside
  AVL event callbacks (prevents concurrent session access).
- `Wialon.remove_avl_event_handler()` — unregister a previously added handler.

### Fixed

- `AvlEventHandler` async context manager cleanup.

## [1.3.1] - 2024-08-13

### Added

- `aiowialon.shortcuts.wlp` — helpers for exporting and importing Wialon `.wlp` resource
  packages.

## [1.3.0] - 2024-08-13

### Added

- Polling now runs as an `asyncio.Task` via `start_polling()` / `stop_polling()`.
- Advanced AVL event handlers with per-handler filter functions.
- `batch()` decorator — collect multiple `call()` coroutines into a single Wialon batch
  request.
- `multipart()` decorator — send file uploads alongside API calls.
- Per-request rate limiting (`aiolimiter`).
- Debug logging via standard `logging` module.
- Full type annotations on all public methods and API response types.
- `prepare_action_name` convention: Python method names (`core_search_items`) are
  automatically mapped to Wialon service names (`core/search_items`).
- Recursive response validation and structured exception hierarchy.
- File download support (binary response handling).

### Changed

- Flags refactored into typed `IntFlag` enumerations.
- All types restructured and documented.
- `https` default port corrected.

### Fixed

- `asyncio` event loop compatibility fixes.
- Suppressed `RuntimeWarning: coroutine was never awaited` in `AvlEventHandler`.
- Batch request exception handling is now recursive.

## [1.2.5] - 2024-03-05

### Changed

- Build system updated to `setuptools` + `setuptools-scm`.

[Unreleased]: https://github.com/o-murphy/py-aiowialon/compare/v2.0.0b2...HEAD
[2.0.0b2]: https://github.com/o-murphy/py-aiowialon/compare/v2.0.0b1...v2.0.0b2
[2.0.0b1]: https://github.com/o-murphy/py-aiowialon/compare/v1.3.5...v2.0.0b1
[1.3.5]: https://github.com/o-murphy/py-aiowialon/compare/v1.3.4.post1...v1.3.5
[1.3.4.post1]: https://github.com/o-murphy/py-aiowialon/compare/v1.3.3...v1.3.4.post1
[1.3.3]: https://github.com/o-murphy/py-aiowialon/compare/v1.3.2...v1.3.3
[1.3.2]: https://github.com/o-murphy/py-aiowialon/compare/v1.3.1...v1.3.2
[1.3.1]: https://github.com/o-murphy/py-aiowialon/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.com/o-murphy/py-aiowialon/compare/v1.2.5...v1.3.0
[1.2.5]: https://github.com/o-murphy/py-aiowialon/commits/v1.2.5
