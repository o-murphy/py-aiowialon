import asyncio
import logging
from datetime import datetime

from aiowialon import Wialon, flags, AvlEvent, WialonError

logging.basicConfig(level=logging.INFO)


class WialonWithCriticalMethod(Wialon):

    async def critical_method(self):
        @self.session_lock
        async def locked_task():
            for i in range(5):
                print("Waiting lock release", i)
                await asyncio.sleep(1)

        return await locked_task()


# Wialon SDK playground token
TEST_TOKEN = '5dce19710a5e26ab8b7b8986cb3c49e58C291791B7F0A7AEB8AFBFCEED7DC03BC48FF5F8'
wialon = WialonWithCriticalMethod(token=TEST_TOKEN)


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


@wialon.avl_event_handler()
@wialon.session_lock
async def unit_event(event: AvlEvent):
    try:
        await wialon.wait(wialon.messages_load_last(
            itemId=event.data.i,
            lastTime=event.tm,
            lastCount=10000,
            flags=0x0000,
            flagsMask=0xFF00,
            loadCount=10000
        ), 10)
    except (TimeoutError, WialonError) as err:
        print(err)
    for i in range(5):
        print("Waiting exclusive operation", i, "item:", event.data.i)
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(wialon.start_polling())
