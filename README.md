# AIO Wialon
`AIO Wialon` is an async implementation of Python wrapper for Wialon Remote API, 
_forked from https://github.com/wialon/python-wialon._

### Table of 
* [Installation](#installation)
* [Start Polling](#start-polling)
* [Wialon API Call](#wialon-api-call)
  * [API Call Example](#api-call-example)
  * [Batch requests](#batch-requests)
  * [Multipart requests](#multipart-requests)
* [Wialon Events](#wialon-events)
  * [On login/logout]()
  * [Register AVL Events]()
  * [AVL Events Handling]()
* [Quick API Help](#quick-api-help)
* [Advanced]()
  * [Wialon Extending]()
  * [Critical requests]()
  * [Limitations]()
  * [Debug]()
  
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

wialon = Wialon()

async def some_func(params1, params2):
    api_calls = [
        wialon.core_search_item(**params1),
        wialon.unit_get_fuel_settings(**params2),
        ...
    ]
    return await wialon.batch(*api_calls, flags_=flags.BatchFlag.EXECUTE_ALL)
```
> [!TIP]
> You can combine different API services and actions in single batch call

> [!WARNING]
> Some requests not support batch!
> Don't try to put batch into other batch, it can raise unexpected behaviour
> Go to the [Wialon Remote Api documentation](http://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/apiref) to get details

### Multipart requests
Use `Wialon.multipart` method and `MultipartField` with API call to but multipart data to request,
Put call coroutine and required MultipartField instances to the `Wialon.multipart()`
```python
from aiowialon import Wialon, MultipartField

wialon = Wialon()

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
> Don't try to put multipart requests to batch!
> Some requests don't support multipart
> Don't try to put multipart request into batch, it can raise unexpected behaviour
> Go to the [Wialon Remote Api documentation](http://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/apiref) to get details


> [!WARNING]
> ### RISK NOTICE
> THE CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE MATERIALS OR THE USE OR OTHER DEALINGS IN THE MATERIALS.


