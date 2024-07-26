"""
Poling example
"""
import asyncio

from aiowialon import Wialon, WialonError, WialonEvent
from aiowialon.types import flags


WIALON_HOST = 'TEST HOST'
WIALON_TOKEN = 'TEST TOKEN'
wialon = Wialon(host=WIALON_HOST, token=WIALON_TOKEN)


async def update_data_flags():
    spec = {
        'itemsType': 'avl_unit',
        'propName': 'sys_name',
        'propValueMask': '*',
        'sortType': 'sys_name'
    }
    interval = {"from": 0, "to": 100}
    units = await wialon.core_search_items(spec=spec, force=1, flags=5, **interval)
    if 'items' in units:
        spec = [
            {
                "type": "col",
                "data": [u['id'] for u in units['items']],
                "flags": flags.UnitsDataFlag.BASE | flags.UnitsDataFlag.POS,
                "mode": 0
            }
        ]
        await wialon.core_update_data_flags(spec=spec)


@wialon.event_handler()
async def handle_event(event: WialonEvent):
    ...


async def main():
    wialon.on_session_open(callback=update_data_flags())

    try:
        wialon.start_poling(token=WIALON_TOKEN)
    except WialonError:
        pass


# def run():
#     """
#     Poling example
#     """
#
#     wialon_session = Wialon(host='TEST HOST', token='TEST TOKEN')

    async def session_did_open():
        spec = {
            'itemsType': 'avl_unit',
            'propName': 'sys_name',
            'propValueMask': '*',
            'sortType': 'sys_name'
        }
        interval = {"from": 0, "to": 100}
        units = await wialon_session.core_search_items(spec=spec, force=1, flags=5, **interval)
        if 'items' in units:
            ids = [u['id'] for u in units['items']]

            spec = [
                {
                    "type": "col",
                    "data": ids,
                    "flags": flags.ITEM_DATAFLAG_BASE + flags.ITEM_UNIT_DATAFLAG_POS,
                    "mode": 0
                }
            ]
            await wialon_session.core_update_data_flags(spec=spec)

    # @wialon_session.event_handler
    # async def event_handler(event: WialonEvent):
    #     if 116106 in events.events:
    #         item_event: WialonEvent = events.events[116106]
    #         print(item_event.item, item_event.e_type, item_event.desc)
    #
    # @wialon_session.event_handler
    # async def event_handler(event: WialonEvent):
    #     spec = {
    #         'itemsType': 'avl_unit',
    #         'propName': 'sys_name',
    #         'propValueMask': '*',
    #         'sortType': 'sys_name'
    #     }
    #     interval = {"from": 0, "to": 0}
    #     units = await wialon_session.core_search_items(spec=spec, force=1, flags=5, **interval)
    #     print(events.__dict__, units['totalItemsCount'])



if __name__ == '__main__':
    asyncio.run(main())
