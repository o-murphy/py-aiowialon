import asyncio

from aiowialon.api import Wialon
from aiowialon.types import flags
from aiowialon.types.avl_events import AvlEvent
import logging

logging.basicConfig(level=logging.INFO)

# Wialon SDK playground token
TEST_TOKEN = '5dce19710a5e26ab8b7b8986cb3c49e58C291791B7F0A7AEB8AFBFCEED7DC03BC48FF5F8'
wialon = Wialon(token=TEST_TOKEN)


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


@wialon.on_session_close
async def on_session_close(session_logout):
    print("Logout event:", session_logout)


@wialon.avl_event_handler(lambda event: True)
async def unit_event(event: AvlEvent):
    print("Handler got event:", event)


if __name__ == "__main__":
    asyncio.run(wialon.start_polling(logout_finally=True))
