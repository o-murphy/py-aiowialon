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
async def register_avl_events(session):
    print("Session eid:", session['eid'])
    spec = [
        {
            "type_": "type",
            "data": "avl_unit",
            "flags": flags.UnitsDataFlag.BASE | flags.UnitsDataFlag.POS,
            "mode": 0
        }
    ]
    c = wialon.core_update_data_flags(spec=spec)
    return await wialon.batch(c)


@wialon.event_handler(lambda event: True)
async def unit_event(event: AvlEvent):
    print("Handler got event:", event)


async def main() -> None:
    poll = asyncio.create_task(wialon.start_polling())
    await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(
        main()
    )
