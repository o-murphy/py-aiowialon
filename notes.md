#### Todos:
- [x] http requests queue
- [x] http requests rate limit
- [x] Automatic calls batching
- [X] Prevent batch for some calls (won't fix, server-side resolved, server throws an acceptable error that we catch)
- [x] Allow multipart
- [x] add logging
- [x] create separate Wialon exceptions
- [x] add WialonError emitter (e.g. aiohttp.ClientResponse.raise_for_status(), use aiowialon.validators)
- [x] wildcard imports (aka. __all__)
- [x] update Docstrings
- [x] update README
- [x] persistent aiohttp.ClientSession (single session per login lifecycle)
- [x] queue-based AVL event dispatch (replaced unbounded create_task fan-out)
- [x] replace frame inspection in ExclusiveAsyncLock with contextvars.ContextVar
- [x] py.typed marker (PEP 561)
- [x] unit tests (pytest + pytest-asyncio, 110 tests)
- [x] CI workflow (test.yml + publish.yml with workflow_call)

- [x] [Report column value types](https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/report/value_types)
- [ ] [Other requests](https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/requests/requests)
- [ ] [Data format](https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/format/format)
- [ ] Other flags/types
- [ ] multiple on_session_open/on_session_close callbacks (currently limited to one each)
- [ ] maybe Pydantic?
- [ ] multiple sessions?
- [x] example of export/import .wlp (now in `shortcuts`)
- [x] added exclusive async lock for long critical operations

#### Autogenerate stubs:
```shell
uv add --dev mypy
uv run stubgen -p aiowialon -o stubs/
```
