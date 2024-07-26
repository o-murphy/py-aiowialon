import asyncio


class EventHandler:
    def __init__(self, callback, filter_):
        self.callback = callback
        self.filter = filter_

    async def __call__(self, event):
        if self.filter(event):
            await self.callback(event)
            return True
        return False


class Client:

    def __init__(self):
        self.__handlers = {}
        self.__on_open = None

    def event_handler(self, filter_):
        def decorator(callback):
            handler = EventHandler(callback, filter_)
            if callback.__name__ in self.__handlers:
                raise KeyError(f"Detected EventHandler duplicate {callback}")
            self.__handlers[callback.__name__] = handler
            return callback  # Return the original callback

        return decorator

    def on_session_open(self):
        def decorator(callback):
            if callback and not callable(callback):
                raise TypeError("on_session_open callback must be callable")
            self.__on_open = callback
            return callback

        return decorator

    async def poll(self):
        event = 'hello'
        while True:
            for name, handler in self.__handlers.items():
                if await handler(event):
                    break
            await asyncio.sleep(1)
            event = 'helloworld' if event == 'hello' else 'hello'


c = Client()


@c.event_handler(filter_=lambda event: event.startswith('hello'))
async def hello(event):
    print("Handled event: {}".format(event))


@c.event_handler(filter_=lambda event: event == 'helloworld')
async def helloworld(event):
    print("Handled event: {}".format(event))


@c.on_session_open
async def on_session_open(self):
    print("Session opened")


async def main():
    await c.poll()


asyncio.run(main())
