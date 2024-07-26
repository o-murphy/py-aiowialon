import asyncio

from aiowialon.api import Wialon
from aiowialon.types import flags
from aiowialon.types.event import AvlEvent

# Wialon SDK playground token
TEST_TOKEN = '5dce19710a5e26ab8b7b8986cb3c49e58C291791B7F0A7AEB8AFBFCEED7DC03BC48FF5F8'
wialon = Wialon(token=TEST_TOKEN)


@wialon.on_session_open
async def register_avl_events():
    spec = {
        'itemsType': 'avl_unit',
        'propName': 'sys_name',
        'propValueMask': '*',
        'sortType': 'sys_name'
    }
    interval = {"from": 0, "to": 100}
    units = await wialon.core_search_items(spec=spec, force=1, flags=5, **interval)
    if 'items' in units:
        ids = [u['id'] for u in units['items']]

        spec = [
            {
                "type": "col",
                "data": ids,
                "flags": flags.UnitsDataFlag.BASE | flags.UnitsDataFlag.POS,
                "mode": 0
            }
        ]
        await wialon.core_update_data_flags(spec=spec)


@wialon.event_handler(lambda event: True)
async def unit_event(event: AvlEvent):
    print("Handler got event:", event)


async def main():
    """
    Poling example
    """
    wialon.start_poling()
    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
