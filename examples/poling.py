import asyncio

from aiowialon.api import Wialon
from aiowialon.types import flags
from aiowialon.types.event import WialonEvents, WialonEvent

wialon = Wialon(host='TEST HOST', token='TEST TOKEN')


async def session_did_open():
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
                "flags": flags.UnitsDataFlag.BASE + flags.UnitsDataFlag.POS,
                "mode": 0
            }
        ]
        await wialon.core_update_data_flags(spec=spec)


@wialon.event_handler
async def event_handler(events: WialonEvents):
    if 116106 in events.data:
        item_event: WialonEvent = events.data[116106]
        print(item_event.item, item_event.e_type, item_event.desc)


@wialon.event_handler
async def event_handler(events: WialonEvents):
    spec = {
        'itemsType': 'avl_unit',
        'propName': 'sys_name',
        'propValueMask': '*',
        'sortType': 'sys_name'
    }
    interval = {"from": 0, "to": 0}
    units = await wialon.core_search_items(spec=spec, force=1, flags=5, **interval)
    print(events.__dict__, units['totalItemsCount'])


async def main():
    """
    Poling example
    """
    wialon.session_did_open(callback=session_did_open)
    wialon.start_poling()


if __name__ == "__main__":
    asyncio.run(main())
