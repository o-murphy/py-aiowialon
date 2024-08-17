import asyncio


class A:

    def __init__(self):
        self.timeout = 2

    async def wait(self, call, timeout):
        prev_timeout = self.timeout
        if timeout:
            self.timeout = timeout
        try:
            return await call
        finally:
            self.timeout = prev_timeout

a = A()

async def c():
    print(a.timeout)
    await asyncio.sleep(3)

async def f():
    print(a.timeout)
    await a.wait(c(), 10)
    print(a.timeout)

asyncio.run(f())