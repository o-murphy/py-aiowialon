import asyncio
from aiowialon import Wialon
from aiowialon.shortcuts.wlp import WLP


async def export_n_import_unit():
    try:
        await wialon.login()
        data = await WLP.export_item(wialon, 27782590)
        await WLP.import_item(wialon, data)
        print(await wialon.avl_evts())
    finally:
        await wialon.logout()


if __name__ == '__main__':
    TEST_TOKEN = '5dce19710a5e26ab8b7b8986cb3c49e58C291791B7F0A7AEB8AFBFCEED7DC03BC48FF5F8'
    wialon = Wialon(token=TEST_TOKEN)
    asyncio.run(export_n_import_unit())
