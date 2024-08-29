import asyncio

from aiowialon import Wialon
from aiowialon.services import WialonCore

w = Wialon(token='5dce19710a5e26ab8b7b8986cb3c49e58C291791B7F0A7AEB8AFBFCEED7DC03BC48FF5F8')
core = WialonCore(w)
w.core = core


async def main():
    try:
        await w.login()
    finally:
        print(await w.batch(w.core._logout()))


asyncio.run(main())
