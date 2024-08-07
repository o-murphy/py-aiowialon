import asyncio
import io
import json
import re

import aiohttp


async def fetch(url, payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload) as response:
            # print(response.content)
            # print(response.headers)
            content_disposition = response.headers.get('Content-Disposition')
            if content_disposition:
                # Extract filename using a regex
                match = re.search(r'filename="(.+)"', content_disposition)
                if match:
                    filename = match.group(1)

            # Read the response content into a buffer
            buffer = io.BytesIO()
            while True:
                chunk = await response.content.read(1024)  # Read in chunks of 1024 bytes
                if not chunk:
                    break
                buffer.write(chunk)

            # To access the buffer content, you can use buffer.getvalue()
            buffer.seek(0)  # Go to the beginning of the buffer
            content = buffer.getvalue()
            print(content)

            with open(filename, 'wb') as file:
                while True:
                    chunk = await response.content.read(1024)  # Read in chunks of 1024 bytes
                    if not chunk:
                        break
                    file.write(chunk)

            # Open a FileIO object for writing
            with io.FileIO('downloaded_file', 'wb') as file:
                while True:
                    chunk = await response.content.read(1024)  # Read in chunks of 1024 bytes
                    if not chunk:
                        break
                    file.write(chunk)

            print('File saved as downloaded_file')

async def main():
    url = 'https://hst-api.wialon.com/wialon/ajax.html'
    payload = dict(
        sid='0297ff1137d8bd16e9b6af992308abf2',
        svc='exchange/export_json',
        params=json.dumps({"fileName": "test.wlp", "json": {}})
    )
    await fetch(url, payload)


asyncio.run(main())
