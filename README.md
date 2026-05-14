[![SWUbanner]][SWUdocs]

[SWUbanner]:
https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-direct-single.svg
[SWUdocs]:
https://github.com/vshymanskyy/StandWithUkraine/blob/main/docs/README.md


# AIO Wialon
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://opensource.org/licenses/MIT)
[![pypi version](https://img.shields.io/pypi/v/py-aiowialon)](https://pypi.org/project/py-aiowialon/)
[![Test](https://github.com/o-murphy/py-aiowialon/actions/workflows/test.yml/badge.svg)](https://github.com/o-murphy/py-aiowialon/actions/workflows/test.yml)

`AIO Wialon` is an async Python wrapper for the Wialon Remote API.

### Table of Contents
- [AIO Wialon](#aio-wialon)
    - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [With uv](#with-uv)
    - [With pip](#with-pip)
  - [Start Polling](#start-polling)
  - [Wialon API Call](#wialon-api-call)
      - [API Call Example](#api-call-example)
    - [Batch requests](#batch-requests)
    - [Multipart requests](#multipart-requests)
    - [Shortcuts](#shortcuts)
  - [Wialon Events](#wialon-events)
    - [Register AVL Events](#register-avl-events)
    - [On login/logout](#on-loginlogout)
    - [AVL Events Handling](#avl-events-handling)
      - [Register AVL Events handlers](#register-avl-events-handlers)
      - [Remove AVL Events handlers](#remove-avl-events-handlers)
      - [Disposable handlers](#disposable-handlers)
  - [Exceptions Handling](#exceptions-handling)
    - [Exceptions Handling (Batch)](#exceptions-handling-batch)
  - [Quick API Help](#quick-api-help)
  - [Advanced usage](#advanced-usage)
    - [Limitations](#limitations)
    - [Context manager](#context-manager)
    - [Prevent polling logout](#prevent-polling-logout)
    - [Critical requests execution](#critical-requests-execution)
      - [Async session lock](#async-session-lock)
      - [Timeout for API call](#timeout-for-api-call)
    - [Extending AIO Wialon](#extending-aio-wialon)
    - [Debugging](#debugging)

## Installation

### With uv
```bash
uv add py-aiowialon
```

### With pip
```bash
pip install py-aiowialon
```

## Start Polling
Open session and start polling AVL events immediately.
[Look the Wialon Events section](#wialon-events) to see how to handle AVL Events during polling.
```python
import asyncio
from aiowialon import Wialon

TOKEN = '<Your Wialon API access token>'
HOST = '<API host IP or url>'
wialon = Wialon(host=HOST, token=TOKEN)

if __name__ == "__main__":
    asyncio.run(wialon.start_polling())
```
> [!TIP]
> `Wialon.start_polling()` does not require a manual `Wialon.login()` call.

## Wialon API Call
Almost all Wialon Remote API `services/actions` are available through dot syntax:
`wialon.<service>_<action_name>(**params)`

Replace `/` with `_` to map an API endpoint to a method name.

#### API Call Example
```python
import asyncio
from aiowialon import Wialon, flags

TOKEN = '<Your Wialon API access token>'
wialon = Wialon(token=TOKEN)

async def main():
    await wialon.login()
    # core/search_item API call:
    result = await wialon.core_search_item(id=12345, flags=flags.UnitsDataFlag.ALL)
    print(result)
    await wialon.logout()

asyncio.run(main())
```

> [!WARNING]
> Some Wialon Remote API methods require exclusive session access
> (report execution, message loading, etc.).
> If you need these methods,
> read the [**Critical requests execution**](#critical-requests-execution) section first.

### Batch requests
Use `Wialon.batch` instead of `asyncio.gather` to make multiple API calls in one request.
This avoids hitting server request limits and moves async overhead to the server side.
```python
from aiowialon import Wialon, flags

wialon = Wialon(token=TOKEN)

async def some_func(params1, params2):
    api_calls = [
        wialon.core_search_item(**params1),
        wialon.unit_get_fuel_settings(**params2),
        ...
    ]
    return await wialon.batch(*api_calls, flags_=flags.BatchFlag.EXECUTE_ALL)
```
> [!TIP]
> * You can combine different API services and actions in a single batch call.
> * [How to handle batch exceptions](#exceptions-handling-batch)

> [!WARNING]
> * Some requests do not support batch!
> * Do not nest batch inside another batch.
> * See the [Wialon Remote API documentation](http://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/apiref) for details.

### Multipart requests
Use `Wialon.multipart` with `MultipartField` to send multipart data.
```python
from aiowialon import Wialon, MultipartField

wialon = Wialon(token=TOKEN)

async def upload_driver_image():
    event_hash = 'aiowialon_drv_upd'
    params = {"itemId": 717351, "driverId": 38, "eventHash": event_hash}
    with open("driver_img.jpg", 'rb') as f:
        file_data = f.read()

    await wialon.multipart(
        wialon.resource_upload_driver_image(**params),
        MultipartField(
            name='drivers_dlg_props_upload_image',
            value=file_data,
            filename="image.jpg",
            content_type='image/jpeg'
        )
    )
```
> [!WARNING]
> * Do not put multipart requests inside a batch.
> * Some requests do not support multipart.
> * See the [Wialon Remote API documentation](http://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/apiref) for details.

### Shortcuts
Shortcuts are pre-built helpers for common operations, such as `.wlp` export.

```python
from aiowialon import Wialon, WLP

wialon = Wialon(token=TOKEN)

async def dump_unit(item_id):
    await wialon.login()
    wlp = await WLP.export_item(wialon, item_id)
    with open(f"{item_id}.wlp", 'wb') as fp:
        fp.write(wlp)
```

## Wialon Events
The library uses polling to handle AVL Events — events that occur on the server and are
returned when registered for the current session.
See [Wialon AVL Events Docs](https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/requests/avl_evts).

### Register AVL Events
Register items for AVL event handling in the current session.
_[(api reference)](https://sdk.wialon.com/wiki/en/sidebar/remoteapi/codesamples/update_datafalags)_

```python
from aiowialon import Wialon, flags

wialon = Wialon(token=TOKEN)

async def register_avl_events():
    spec = [
        {
            "type": "type",
            "data": "avl_unit",
            "flags": flags.UnitsDataFlag.BASE | flags.UnitsDataFlag.POS,
            "mode": 0
        }
    ]
    return await wialon.core_update_data_flags(spec=spec)
```

### On login/logout
Use `@wialon.on_session_open` to run logic automatically after each login.
```python
@wialon.on_session_open
async def register_avl_events(session_login):
    print("Session eid:", session_login['eid'])
    spec = [
        {
            "type": "type",
            "data": "avl_unit",
            "flags": flags.UnitsDataFlag.BASE | flags.UnitsDataFlag.POS,
            "mode": 0
        }
    ]
    return await wialon.core_update_data_flags(spec=spec)

if __name__ == "__main__":
    asyncio.run(wialon.start_polling())
```

Use `@wialon.on_session_close` to run logic after logout:
```python
@wialon.on_session_close
async def on_session_close(session_logout):
    print("Logout event:", session_logout)
```
> [!NOTE]
> * Only one `on_session_open` callback can be registered per `Wialon` instance.
> * Only one `on_session_close` callback can be registered per `Wialon` instance.


### AVL Events Handling
After polling starts and AVL items are registered, use `@wialon.avl_event_handler()` to handle events.

Each handler runs its callback in a **sequential queue** — events for a given handler are
processed one at a time, in order, without unbounded parallelism.

#### Register AVL Events handlers
```python
from aiowialon import AvlEvent


@wialon.avl_event_handler()
async def unit_event(event: AvlEvent):
    print("Handler got event:", event)
```

Apply a filter to handle only matching events:
```python
from aiowialon import AvlEvent


@wialon.avl_event_handler(lambda event: event.data.i == 734455)
async def unit_734455_event(event: AvlEvent):
    print("Handler got event from item 734455:", event)
```
> [!NOTE]
> Handlers are checked in registration order. Once a handler accepts an event (filter matches),
> subsequent handlers are skipped for that event.

#### Remove AVL Events handlers
```python
wialon.remove_avl_event_handler('handler_name')
wialon.remove_avl_event_handler(handler_func)
```

#### Disposable handlers
Use `@wialon.avl_event_once` to automatically remove a handler after its first execution.
```python
@wialon.avl_event_handler()
@wialon.avl_event_once
async def unit_event(event: AvlEvent):
    print("Handler got event:", event)
```


## Exceptions Handling
`avl_event_handler` catches and logs `WialonError` and `aiohttp.ClientError` from callbacks
to prevent a single failure from stopping the polling loop.
Handle specific errors inside the callback scope if needed.

> [!NOTE]
> You can still access response data even when `WialonError` is raised — [see below](#exceptions-handling-batch).

```python
from aiowialon import WialonError, WialonAccessDenied


@wialon.avl_event_handler()
async def unit_event(event: AvlEvent):
    try:
        await wialon.core_search_item(id=event.data.i, flags=1)
    except WialonAccessDenied as err:
        print("Access denied:", err)
    except WialonError as err:
        print("Wialon error:", err)
```

### Exceptions Handling (Batch)
`WialonError.reason` returns a string for single calls or `list[WialonError]` for batch calls.
`WialonError.result` carries the raw response data.
```python
async def some_func():
    result = None
    try:
        result = await wialon.batch(*calls, flags_=flags.BatchFlag.STOP_ON_ERROR)
    except WialonError as err:
        print("Errors", err.reason)  # list[WialonError] for batch
        result = err.result
    finally:
        print("Result", result)
```


## Quick API Help
Open Wialon Remote API docs in your browser:
```python
from aiowialon import Wialon

Wialon.help('core', 'search_item')
```


## Advanced usage

### Limitations
The client is limited to 10 concurrent connections via `asyncio.Semaphore` and to 10 requests
per second via `aiolimiter`, matching Wialon API server limits.
Adjust `rps` to match your account tier:
```python
from aiowialon import Wialon
wialon = Wialon(rps=15)
```

### Context manager
`Wialon` supports use as an async context manager, which ensures the underlying HTTP session
is closed cleanly even if an exception occurs:
```python
async def main():
    async with Wialon(token=TOKEN) as wialon:
        await wialon.login()
        result = await wialon.core_search_item(id=12345, flags=1)
        print(result)
        await wialon.logout()
```

### Prevent polling logout
By default `start_polling` logs out when stopped or on exception. Disable with `logout_finally=False`:
```python
from aiowialon import Wialon
wialon = Wialon(token=TOKEN)
asyncio.run(wialon.start_polling(logout_finally=False))
```

### Critical requests execution

#### Async session lock
Some API calls (reports, messages, render) must run exclusively — no other requests should
be sent to the same session concurrently.
Use `@wialon.session_lock` to block the session until the decorated coroutine completes.

```python
import asyncio
from aiowialon import Wialon

wialon = Wialon(token=TOKEN)


@wialon.session_lock
async def run_report(params1, params2):
    try:
        wialon.timeout = 600  # reports can take a long time
        await wialon.report_exec_report(**params1)
        return await wialon.report_export_result(**params2)
    finally:
        wialon.timeout = 5
        await wialon.report_cleanup_result()
```

With event handlers:
```python
@wialon.avl_event_handler(lambda event: event.data.i == 734455)
@wialon.session_lock
async def unit_event(event: AvlEvent):
    print("Handler got event:", event)
    for i in range(5):
        print("Exclusive operation in progress:", i)
        await asyncio.sleep(1)
```


#### Timeout for API call
Use `Wialon.wait()` to set a per-call timeout without changing the global default:
```python
@wialon.avl_event_handler()
@wialon.session_lock
async def unit_event(event: AvlEvent):
    try:
        messages = await wialon.wait(
            wialon.messages_load_last(
                itemId=event.data.i,
                lastTime=event.tm,
                lastCount=10000,
                flags=0x0000,
                flagsMask=0xFF00,
                loadCount=10000,
            ),
            timeout=30,
        )
    except (TimeoutError, WialonError) as err:
        print(err)
```


### Extending AIO Wialon
Inherit from `Wialon` to add custom logic. Use `self.request()` for direct HTTP calls and
`@self.session_lock` for exclusive access:

```python
import json
import asyncio
from aiowialon import Wialon


class CustomWialon(Wialon):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        scheme = kwargs.get('scheme', 'https')
        host = kwargs.get('host', 'hst-api.wialon.com')
        self._geocode_url = f"{scheme}://geocode-maps.wialon.com/{host}/gis_geocode"

    async def geocode_address(self, coords, city_radius, dist_from_unit, txt_dist, flags):
        payload = json.dumps({
            'coords': coords,
            'cityRadius': city_radius,
            'distFromUnit': dist_from_unit,
            'txtDist': txt_dist,
            'flags': flags,
        })
        return await self.request('gis_geocode', self._geocode_url, payload)

    async def critical_method(self):
        @self.session_lock
        async def locked_task():
            for i in range(5):
                print("Exclusive operation:", i)
                await asyncio.sleep(1)
        return await locked_task()
```

### Debugging
Enable debug logging for `aiowialon` and `aiohttp.client`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

> [!WARNING]
> ### RISK NOTICE
> THE CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE MATERIALS OR THE USE OR OTHER DEALINGS IN THE MATERIALS.

*Copyright 2023 Yaroshenko Dmytro (https://github.com/o-murphy)*
