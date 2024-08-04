import asyncio

from aiowialon.api import Wialon
from aiowialon.exceptions import WialonError

wialon = Wialon(host='TEST HOST', token='TEST TOKEN')


async def main():
    """
    Example of manual using
    """
    try:
        result = await wialon.login()
        wialon.sid = result['eid']
        await wialon.avl_evts()
        await wialon.core_logout()
    except WialonError:
        pass


if __name__ == "__main__":
    asyncio.run(main())
