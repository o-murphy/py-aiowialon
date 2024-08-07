- [x] http requests queue
- [x] http requests rate limit
- [x] Automatic calls batching
- [X] Prevent batch for some calls (won't fix, server-side resolved, server throws en exceptable error that we catch)
- [ ] Allow multipart
- [ ] update README
- [x] add logging
- [x] create separate Wialon exceptions
- [x] add WialonError emitter (e.g. aiohttp.ClientResponse.raise_for_status(), use aiowialon.validators)
- [x] wildcard imports (aka. __all__)

- [x] [Report column value types](https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/report/value_types)
- [ ] [Other requests](https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/requests/requests)
- [ ] [Data format](https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/format/format)
- [ ] Other flags/types

```shell
# autogenerate stubs
pip install mypy
stubgen -m your_module -o output_directory
```
