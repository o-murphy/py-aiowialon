# AIO Wialon
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://opensource.org/licenses/MIT)
[![pypi version](https://img.shields.io/pypi/v/py-aiowialon)](https://pypi.org/project/py-aiowialon/)

`AIO Wialon` is an async implementation of Python wrapper for Wialon Remote API, 

### Table of 
* [Installation](#installation)
* [Start Polling](#start-polling)
* [Wialon API Call](#wialon-api-call)
  * [API Call Example](#api-call-example)
  * [Batch requests](#batch-requests)
  * [Multipart requests](#multipart-requests)
* [Wialon Events](#wialon-events)
  * [Register AVL Events](#register-avl-events)
  * [On login/logout](#on-loginlogout)
  * [AVL Events Handling](#avl-events-handling)
* [Exceptions Handling](#exceptions-handling)
  * [Get exception results, batch exceptions](#exceptions-handling-batch)
* [Quick API Help](#quick-api-help)
* [Advanced](#advanced-usage)
  * [Limitations](#limitations)
  * [Prevent polling auto logout](#prevent-polling-logout)
  * [Critical sections (Render, Reports, Messages)](#critical-sections)
  * [Extending AIO Wialon](#extending-aio-wialon)
  * [Debugging](#debugging)
  
* [Wialon Remote Api documentation](http://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/apiref)

## Installation
```bash
pip install py-aiowialon
```

## Start Polling
Open session and start poll AVL events immediately
[Look the Wialon Events section](#wialon-events) to see how we can handle AVL Events on polling
```python
import asyncio
from aiowialon import Wialon

TOKEN = '<Your Wialon API access token>'
HOST = '<API host IP or url>'
wialon = Wialon(host=HOST, token=TOKEN)

if __name__ == "__main__":
    asyncio.run(wialon.start_polling())
```
> [!Note]
> `Wialon.start_polling()` is not require a manual Wialon.login() call 

## Wialon API Call
API Call is function that returns `Wialon.call()` instance
Almost all Wialon Remote API `services/actions` available 
through dot syntax: `wialon.<service>_<action_name>(**params)`

To make API call use method of Wialon instance with same name as API endpoint
replace `/` with underscore.

#### API Call Example
```python
import asyncio
from aiowialon import Wialon, flags

TOKEN = '<Your Wialon API access token>'
wialon = Wialon(token=TOKEN)

async def main():
    await wialon.login()
    # The example of core/search_item API call:
    result = await wialon.core_search_item(id=12345, flags=flags.UnitsDataFlag.ALL)
    print(result)
    await wialon.logout()

asyncio.run(main())
```

### Batch requests
Use `Wialon.batch` instead of `asyncio.gather` to make multiple API calls in a same time.
It allows to make just one request to server with few calls.
This avoids reaching the server's request limits. 
And transfers the overhead of processing asynchronous context to the server side.
Few Wialon.call() coroutines would be batched to single 'core/batch' request.
```python
# put few calls to a batch method
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
> * You can combine different API services and actions in single batch call
> * [How to handle batch exceptions](#exceptions-handling-batch)

> [!WARNING]
> * Some requests don't support batch!
> * Don't try to put batch into other batch, it can raise unexpected behaviour
> * Go to the [Wialon Remote Api documentation](http://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/apiref) to get details

### Multipart requests
Use `Wialon.multipart` method and `MultipartField` with API call to but multipart data to request,
Put call coroutine and required MultipartField instances to the `Wialon.multipart()`
```python
from aiowialon import Wialon, MultipartField

wialon = Wialon(token=TOKEN)

async def upload_driver_image():
    event_hash = 'aiowialon_drv_upd'  # custom event hash
    params = {"itemId": 717351, "driverId": 38, "eventHash": event_hash}
    file_path = "driver_img.jpg"
    with open(file_path, 'rb') as f:
        file_data = f.read()

    await wialon.multipart(
        wialon.resource_upload_driver_image(**params),
        *[
            MultipartField(
                name='drivers_dlg_props_upload_image',
                value=file_data,
                filename="image.jpg",
                content_type='image/jpeg'
            )
        ]
    )
```
> [!WARNING]
> * Don't try to put multipart requests to batch!
> * Some requests don't support multipart
> * Don't try to put multipart request into batch, it can raise unexpected behaviour
> * Go to the [Wialon Remote Api documentation](http://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/apiref) to get details


## Wialon Events
The library propose using the polling to handle AVL Events.
AVL events is the events that happens on the server and returns to us if we registered it in current session
This section references to [Wialon AVL Events Docs](https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/requests/avl_evts)

### Register AVL Events
Firstly we have to register items for AVL events handling in current session.
_[(api reference here)](https://sdk.wialon.com/wiki/en/sidebar/remoteapi/codesamples/update_datafalags)_

Bellow is example how to add all AVL Units (vehicles) to handle AVL events of this units in current session,
We use there just simple Wialon API Call
```python
from aiowialon import Wialon, flags

wialon = Wialon(token=TOKEN)

async def register_avl_events():
    spec = [
        {
            "type_": "type",
            "data": "avl_unit",
            "flags": flags.UnitsDataFlag.BASE | flags.UnitsDataFlag.POS,
            "mode": 0
        }
    ]
    return await wialon.core_update_data_flags(spec=spec)
```

### On login/logout
We can automate this logic for each session opening by registering `on_session_open` callback,
Use `@wialon.on_session_open` decorator for this
So wialon will login and register avl items to polling before polling start
```python
@wialon.on_session_open
async def register_avl_events(session_login):
    print("Session eid:", session_login['eid'])
    spec = [
        {
            "type_": "type",
            "data": "avl_unit",
            "flags": flags.UnitsDataFlag.BASE | flags.UnitsDataFlag.POS,
            "mode": 0
        }
    ]
    return await wialon.core_update_data_flags(spec=spec)

if __name__ == "__main__":
    asyncio.run(wialon.start_polling())
```

Also we can add callback on session logout. Use `@wialon.on_session_close` decorator for this

```python
@wialon.on_session_close
async def on_session_close(session_logout):
    print("Logout event:", session_logout)
```
> [!NOTE]
> * You can register just one `on_session_open` callback for Wialon instance
> * You can register just one `on_session_close` callback for Wialon instance


### AVL Events Handling
After polling start and AVL Items registered for polling we can handle the AVL Events.
Use `@wialon.avl_event_handler()` decorator

```python
from aiowialon import AvlEvent

@wialon.avl_event_handler()
async def unit_event(event: AvlEvent):
    print("Handler got event:", event)
```

Put the filter function to the decorator to apply filtering of AVL events
```python
from aiowialon import AvlEvent

@wialon.avl_event_handler(lambda event: event.data.i == 734455)
async def unit_734455_event(event: AvlEvent):
    print("Handler got event from item 734455:", event)
```
> [!NOTE]
> Register handlers in an order in which filters have to be applied. If some handler catched the event, next handler in order will never do.

## Exceptions Handling
The avl_event_handler suppress the callback's WialonError exceptions to protect app to be closed on unexpected behaviour
So if u want to handle some specific WialonError, do it in handler's callback scope

> [!NOTE]
> You still can get access to response data even if WialonError exception was raised, [see next section](#exceptions-handling-batch)

```python
from aiowialon import WialonError, WialonAccessDenied

@wialon.avl_event_handler()
async def unit_event(event: AvlEvent):
    try:
        raise WialonAccessDenied  # example of wialon exception raised in callback scope
    except WialonError as err:
        # do something
        pass
    
```

### Exceptions Handling (Batch)
You still can get access to response data even if WialonError exception was raised
It can be usefull for debug or for the batch requests
`WialonError.reason` returns string for single call or `list[WialonError]` for batch call
```python
async def some_func():
    result = None 
    try:
        result = await wialon.batch(*calls, flags_=flags.BatchFlag.STOP_ON_ERROR)
    except WialonError as err:
        print("Errors", err.reason) # returns a list of WialonErrors for each call in batch
        result = err.result
    finally:
        print("Result", result)
```


### Quick API Help
Use `Wialon.help(service_name, action_name)` to open Wialon Remote API docs in your system browser
```python
from aiowialon import Wialon

Wialon.help('core', 'search_item')
```

## Advanced usage

### Limitations
Adjusting to the Wialon API limitations the Wialon API client limited to 10 connections maximum per session wia `asyncio.semaphore`
Also it limited to 10 requests per second for the session with `aiolimiter`
You can set custom limit of requests per second for your requirements
```python
from aiowialon import Wialon
wialon = Wialon(rps=15)  # set custom requests per second limit
```

### Prevent polling logout
By default `start_polling` autologout on `Exception` or on manual `stop_polling`. You can adjust it to your requirements
```python
from aiowialon import Wialon
wialon = Wialon()  # set custom requests per second limit
wialon.start_polling(token=TOKEN, logout_finally=False)
```

### Debugging
Enable debug messages for `aiowialon` and `aiohttp`
```python
import logging
from aiowialon import Wialon, WialonError, flags, AvlEvent
logging.basicConfig(level=logging.DEBUG)
```

### Extending AIO Wialon
Inherit from `Wialon` class to add your custom logic and behaviour
You can directly use `Wialon.request` to make requests to special endpoints

```python
import json
from aiowialon import Wialon


class WialonWithGeocode(Wialon):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.__geocode_url = f"{kwargs.get('scheme', 'https')}://geocode-maps.wialon.com/{self.__base_url}/gis_geocode"

  async def geocode_address(self, coords, city_radius, dist_from_unit, txt_dist, flags):
    payload = {
      'coords': coords,
      ...  # other fields
    }
    return await self.request('geocode_fetch', self.__geocode_url, payload=json.dumps(payload))
```

### Critical sections
Some requests to services like `Render`, `Reports`, `Messages` requires blocking other requests to be executed together per single session.
Use asyncio lock globally for `Wialon` instance to execute critical requests.

```python
import aiohttp
import asyncio
from aiowialon import Wialon


class WialonWithLock(Wialon):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.session_lock = asyncio.Lock()


wialon = WialonWithLock(token=TOKEN)


async def critical_func():
  await wialon.login()
  async with wialon.session_lock:
    previous_request_timeout = wialon.timeout  # store current timeout
    try:
      wialon.timeout = 600  # setup request timeout up to 10 minutes
      await wialon.report_exec_report(**params1)
      wialon.timeout = previous_request_timeout  # return previous timeout 
      report_result = await wialon.export_result(**params2)
      return report_result
    finally:
      wialon.timeout = previous_request_timeout  # return previous timeout 
      await wialon.report_cleanup_result()
```


> [!WARNING]
> ### RISK NOTICE
> THE CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE MATERIALS OR THE USE OR OTHER DEALINGS IN THE MATERIALS.

*Copyright 2023 Yaroshenko Dmytro (https://github.com/o-murphy)*
