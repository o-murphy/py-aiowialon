- [x] http requests queue
- [x] http requests rate limit
- [ ] Automatic request batching
- [ ] OOP Models for Items
- [ ] Prevent batch for some calls
- [ ] Allow multipart
- [ ] update README
- [x] add logging
- [ ] create separate Wialon exceptions
- [ ] add WialonError emitter (e.g. aiohttp.ClientResponse.raise_for_status())
- [ ] async def call to Call object to create requests/batches

- [ ] [Report column value types](https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/report/value_types)
- [ ] [Other requests](https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/requests/requests)
- [ ] [Data format](https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/format/format)

```shell
# autogenerate stubs
pip install mypy
stubgen -m your_module -o output_directory
```
