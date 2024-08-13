import asyncio
import json

from aiowialon import Wialon, MultipartField
from aiowialon.utils.shortcuts.wlp import WLP


async def export_n_import_unit():
    try:
        await wialon.login()
        data = await WLP.export_item(wialon, 27782590)
        with open('unit.wlp', 'wb') as fp:
            fp.write(data)

        u = json.loads(data)
        u['general']['n'] = 'test_object'
        fileName = f'{u["general"]["n"]}.wlp'
        eventHash = f'ImportAvl_{u["general"]["n"]}'

        await wialon.multipart(
            wialon.exchange_import_json(eventHash=eventHash),
            MultipartField(name='eventHash', value=eventHash),
            MultipartField(name='import_file',
                           value=json.dumps(u),
                           filename=fileName,
                           content_type='application/zip')
        )
        print(await wialon.avl_evts())
    finally:
        await wialon.logout()


if __name__ == '__main__':
    TEST_TOKEN = '5dce19710a5e26ab8b7b8986cb3c49e58C291791B7F0A7AEB8AFBFCEED7DC03BC48FF5F8'
    wialon = Wialon(token=TEST_TOKEN)
    asyncio.run(export_n_import_unit())
