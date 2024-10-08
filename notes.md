#### Todos:
- [x] http requests queue
- [x] http requests rate limit
- [x] Automatic calls batching
- [X] Prevent batch for some calls (won't fix, server-side resolved, server throws en exceptable error that we catch)
- [x] Allow multipart
- [x] add logging
- [x] create separate Wialon exceptions
- [x] add WialonError emitter (e.g. aiohttp.ClientResponse.raise_for_status(), use aiowialon.validators)
- [x] wildcard imports (aka. __all__)
- [x] update Docstrings
- [x] update README

- [x] [Report column value types](https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/report/value_types)
- [ ] [Other requests](https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/requests/requests)
- [ ] [Data format](https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/format/format)
- [ ] Other flags/types
- [ ] maybe Pydantic?
- [ ] multiple sessions?
- [x] example of export/import .wlp (now in `shortcuts`)
- [x] added exclusive async lock for long critical operations

#### Autogenerate stubs:
```shell
pip install -e .[dev]
stubgen -m your_module -o output_directory
```