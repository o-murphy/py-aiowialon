import asyncio
import time
from aiolimiter import AsyncLimiter
from random import random
from tqdm.asyncio import tqdm_asyncio


limiter = AsyncLimiter(10, 1)


completed_tasks = 0
rate_measurements = []


async def unlimited_method(id):
    global prev_waiters, prev_time
    async with limiter:
        return await asyncio.sleep(random())


from tqdm.asyncio import tqdm_asyncio


ref = time.time()
asyncio.run(
    tqdm_asyncio.gather(
        *[unlimited_method(i) for i in range(100)]
    )
)