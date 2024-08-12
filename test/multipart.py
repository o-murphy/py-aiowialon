import asyncio
import json
import os.path

import aiohttp

from aiowialon import Wialon, flags, WialonCallRespValidator
from aiowialon.types.multipart import MultipartField


async def download_wlp():
    await w.login(token='5dce19710a5e26ab8b7b8986cb3c49e58C291791B7F0A7AEB8AFBFCEED7DC03BC48FF5F8')
    item = await w.core_search_item(id=734455, flags=flags.UnitsDataFlag.ALL)
    attachment = await w.exchange_export_json(**{"fileName": "test.wlp", "json": item})
    print("test.wlp", f'{len(attachment)} bytes')


async def direct_upload_driver_image():
    event_hash = 'aiowialon_drv_upd'
    params = {"itemId": 717351, "driverId": 38, "eventHash": event_hash}
    file_path = os.path.join(os.path.dirname(__file__), "drv_img.jpg")

    # Prepare the multipart form data
    form_data = aiohttp.FormData()
    form_data.add_field('sid', w._sid, content_type='application/x-www-form-urlencoded')
    form_data.add_field('svc', 'resource/upload_driver_image',
                        content_type='application/x-www-form-urlencoded')

    # Add the JSON 'params' field
    form_data.add_field('params', json.dumps(params), content_type='application/json')

    # Add the image file
    with open(file_path, 'rb') as f:
        form_data.add_field('n', f.read(), filename="image.jpg", content_type='image/jpeg')

    # Construct the URL with the necessary parameters
    url = f'https://hst-api.wialon.com/wialon/ajax.html'

    # Send the POST request
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=form_data) as response:
            print(response.headers)
            res = await response.json(content_type=None)
            await WialonCallRespValidator.validate_result('drivers_dlg_props_upload_image', res)
            print(res)


async def upload_driver_image():
    event_hash = 'aiowialon_drv_upd'
    params = {"itemId": 717351, "driverId": 38, "eventHash": event_hash}
    file_path = os.path.join(os.path.dirname(__file__), "drv_img.jpg")
    with open(file_path, 'rb') as f:
        file_data = f.read()

    await w.multipart(
        w.resource_upload_driver_image(**params),
        *[
            MultipartField(
                name='drivers_dlg_props_upload_image',
                value=file_data,
                filename="image.jpg",
                content_type='image/jpeg'
            )
        ]
    )


async def main():
    try:
        await w.login(token='5dce19710a5e26ab8b7b8986cb3c49e58C291791B7F0A7AEB8AFBFCEED7DC03BC48FF5F8')
        await download_wlp()
        await upload_driver_image()
    finally:
        await w.logout()

