#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Async Wialon Remote API client implementation"""

import asyncio
import json
import warnings
from contextlib import suppress
from functools import wraps
from typing import Callable, Coroutine, Dict, Optional, Any, Union, Literal, List
from urllib.parse import urljoin

import aiohttp
from aiolimiter import AsyncLimiter

from aiowialon.exceptions import WialonError, WialonRequestLimitExceededError, WialonWarning
from aiowialon.logger import logger, aiohttp_trace_config
from aiowialon.types import (AvlEventHandler, AvlEventFilter, AvlEvent,
                             AvlEventCallback, LogoutCallback)
from aiowialon.types import LoginParams, LoginCallback, flags, MultipartField
from aiowialon.utils.async_lock import ExclusiveAsyncLock
from aiowialon.utils import convention
from aiowialon.utils.compat import Unpack
from aiowialon.validators import WialonCallRespValidator


# pylint: disable=too-many-instance-attributes
class Wialon:
    """
    Async Wialon Remote API client implementation,
    use this for open connection and communicate with Wialon
    """

    # pylint: disable=too-many-arguments
    def __init__(self, scheme: Literal['https', 'http'] = 'https',
                 host: str = "hst-api.wialon.com", port: Optional[int] = None,
                 token: Optional[str] = None, rps: int = 10):
        """
        Creates the Wialon API client instance.
        :param scheme: 'https/http'
        :param host: IP/Url of the Wialon server where an API endpoint placed
        :param port: Port of the Wialon server where an API endpoint placed
        :param token: Wialon API Token
        :param rps: Max requests per second
        """

        self._sid: Optional[str] = None
        self._token: Optional[str] = token
        self._timeout: aiohttp.ClientTimeout = aiohttp.ClientTimeout(total=5)

        self.__base_url = f"{scheme}://{host}:{port if port else 443 if scheme == 'https' else 80}"
        self.__base_api_url: str = urljoin(self.__base_url, 'wialon/ajax.html')

        self.__avl_event_handlers: Dict[str, AvlEventHandler] = {}
        self.__on_session_open: Optional[LoginCallback] = None
        self.__on_session_close: Optional[LogoutCallback] = None

        self.__polling_lock: asyncio.Lock = asyncio.Lock()
        self.__polling_task: Optional[asyncio.Task] = None

        self.__semaphore: asyncio.Semaphore = asyncio.Semaphore(10)
        self.__limiter: AsyncLimiter = AsyncLimiter(rps, 1)

        self.__exclusive_session_lock: ExclusiveAsyncLock = ExclusiveAsyncLock()

    @property
    def token(self) -> Optional[str]:
        """Get current Wialon Remote API access token"""

        return self._token

    @token.setter
    def token(self, token: str) -> None:
        """Update Wialon Remote API access token"""

        self._token = token

    @property
    def timeout(self) -> float:
        """Get current Wialon Client request timeout"""

        return self._timeout.total

    @timeout.setter
    def timeout(self, timeout: float) -> None:
        """Set current Wialon Client request timeout"""

        if not isinstance(timeout, (int, float)):
            raise TypeError("timeout must be an instance of (int, float")
        self._timeout = aiohttp.ClientTimeout(timeout)

    @property
    def session_lock(self) -> Callable:
        """
        Decorator to set exclusive session access for long critical operations

        >>> # Example
        >>> from aiowialon import Wialon
        >>> wialon = Wialon()
        >>>
        >>> @wialon.avl_event_handler()
        >>> @wialon.session_lock  # exclusive session lock for callback's frame
        >>> async def unit_event(event: AvlEvent):
        >>>     await wialon.core_search_item(id=event.data.i, flags=1)
        """

        return self.__exclusive_session_lock.lock

    def on_session_open(self,
                        callback: Optional[LoginCallback] = None) -> Optional[LoginCallback]:
        """
        Decorator to register callback when session open
        WARNING: This decorator can set just single callback for each Wialon instance
        """

        if callback and not callable(callback):
            raise TypeError(f"'on_session_open' callback must be a type of {LoginCallback}")
        if self.__on_session_open is not None:
            warnings.warn(
                "'on_session_open' callback will be override with new one "
                f"'{self.__on_session_open.__qualname__}' -> '{callback.__qualname__}'",
                WialonWarning
            )
        self.__on_session_open = callback
        return callback

    def on_session_close(self,
                         callback: Optional[LogoutCallback] = None) -> Optional[LogoutCallback]:
        """
        Decorator to register callback when session close
        WARNING: This decorator can set just single callback for each Wialon instance
        """

        if callback and not callable(callback):
            raise TypeError(f"'on_session_close' callback must be a type of {LogoutCallback}")
        if self.__on_session_close is not None:
            warnings.warn(
                "'on_session_close' callback will be override with new one "
                f"'{self.__on_session_close.__qualname__}' -> '{callback.__qualname__}'",
                WialonWarning
            )
        self.__on_session_close = callback
        return callback

    def avl_event_handler(self, filter_: Optional[AvlEventFilter] = None) -> Callable:
        """
        Decorator to register multiple AVL event handlers for current Wialon instance
        Set callback and filter function to catch and process AVL events
        """

        def wrapper(callback: AvlEventCallback):
            """
            TODO: maybe add special attribute to callback
            setattr(callback, 'unregister', lambda: self.remove_avl_event_handler(callback))
            >>> @wialon.avl_event_handler()
            >>> @wialon.session_lock  # exclusive session lock for callback's frame
            >>> async def unit_event(event: AvlEvent):
            >>>     # create some request with event hash
            >>>     await wialon.avl_evts(event)
            >>>     unit_event.unregister()  # to be honest that executes just once
            """
            handler = AvlEventHandler(callback, filter_)
            if callback.__name__ in self.__avl_event_handlers:
                raise KeyError(f"Detected AVLEventHandler duplicate {callback.__name__}")
            self.__avl_event_handlers[callback.__name__] = handler
            return callback

        return wrapper

    def avl_event_once(self, func: Optional[Callable[..., Coroutine[Any, Any, Any]]] = None
                       ) -> Callable[..., Coroutine[Any, Any, Any]]:
        """Be certain that handler will be removed after single execution"""

        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            try:
                return await func(*args, **kwargs)
            finally:
                self.remove_avl_event_handler(func)

        return wrapper

    def remove_avl_event_handler(self, callback: Union[str, AvlEventCallback]):
        """
        Manually remove AVL event handler
        :param callback: AvlEventCallback or its string name
        """

        if callable(callback):
            callback = callback.__name__
        if isinstance(callback, str):
            handler = self.__avl_event_handlers.pop(callback)
            handler.cleanup()
        else:
            warnings.warn(f"Can't remove AVL event handler: {callback}")

    async def _process_event_handlers(self, event: AvlEvent) -> None:
        """Process event handlers for current item"""

        for _, handler in self.__avl_event_handlers.items():
            if await handler(event):
                break

    async def _cleanup_event_handlers(self) -> None:
        """Cleanup event handlers"""

        for _, handler in self.__avl_event_handlers.items():
            handler.cleanup()

    async def start_polling(self, timeout: Union[int, float] = 2,
                            logout_finally: bool = True,
                            **params: Unpack[LoginParams]) -> None:
        """Open session and start polling avl events"""

        if timeout < 1:
            raise ValueError("Poling timeout have to be >= 1 second. "
                             "No more than 10 'avl_evts' requests "
                             "can be processed during 10 seconds")

        async with self.__polling_lock:

            await self.login(**params)
            self.__polling_task = asyncio.create_task(self._polling(timeout))
            logger.info("Polling task started")
            try:
                await self.__polling_task
            except asyncio.CancelledError:
                logger.info("Polling task was canceled")
            finally:
                try:
                    await self.stop_polling(logout_finally)
                finally:
                    logger.info("Wialon polling stopped")

    async def stop_polling(self, logout: bool = False) -> None:
        """Execute this method if you want to stop polling programmatically"""

        if not self.__polling_lock.locked():
            raise RuntimeError("Polling is not started")

        if self.__polling_task:
            logger.info("Stopping polling task")
            self.__polling_task.cancel()
            await self._cleanup_event_handlers()
            with suppress(asyncio.CancelledError):
                await self.__polling_task
            self.__polling_task = None
        if logout:
            await self.logout()

    async def login(self, **params: Unpack[LoginParams]) -> Dict[str, Any]:
        """Manually login to Wialon with token or auth hash"""

        token = params.get("token", None)
        auth_hash = params.get("auth_hash", None)
        if token and auth_hash:
            raise ValueError("You can't use both token and auth_hash "
                             "at the same time on login")

        logger.info('Wialon login: %s', self.__base_url)
        if auth_hash:
            session_login = await self.core_use_auth_hash(**params)
        else:
            if token:
                self.token = token
            params['token'] = self.token
            session_login = await self.token_login(**params)

        if isinstance(session_login, dict):
            self._sid = session_login['eid']
            logger.debug("sid: %s", self._sid)
            logger.info("Wialon session opened")
        else:
            raise TypeError(f"Unexpected login response: {session_login}")
        if self.__on_session_open:
            await self.__on_session_open(session_login)
        return session_login

    async def logout(self) -> Any:
        """Attempt to logout"""

        if self._sid:
            logger.info("Wialon logout")
            session_logout = await self.core_logout()
            self._sid = None
            if self.__on_session_close:
                await self.__on_session_close(session_logout)
            return session_logout

    async def _polling(self, timeout: Union[int, float] = 2) -> None:
        """Internal avl event polling loop"""

        while self._sid:
            try:
                response = await self.avl_evts()
                events = AvlEvent.parse_avl_events_response(response)
                await asyncio.gather(*[self._process_event_handlers(event) for event in events])
            except WialonRequestLimitExceededError as err:
                logger.exception(err)
            await asyncio.sleep(timeout)

    async def avl_evts(self) -> Any:
        """Call avl_event request"""

        if self.__polling_task:
            warnings.warn("Polling running, don't recommended to call 'avl_evts' manually",
                          WialonWarning)
        url = urljoin(self.__base_url, 'avl_evts')
        params = {
            'sid': self._sid
        }
        return await self.request('avl_evts', url, params)

    # pylint: disable=unused-argument
    async def call(self, action_name: str, *args: Any, **params: Any) -> Any:
        """Call the API method provided with the parameters supplied."""

        params = convention.prepare_action_params(params)
        payload = json.dumps(params, ensure_ascii=False)
        params = {
            'svc': convention.prepare_action_name(action_name),
            'params': payload,
            'sid': self._sid
        }
        return await self.request(action_name, self.__base_api_url, params)

    async def batch(self, *calls: Coroutine[Any, Any, Any],
                    flags_: flags.BatchFlag = flags.BatchFlag.EXECUTE_ALL) -> List[Any]:
        """Adapter method for list of 'Wialon.call()',
         coroutines to collect them to single batch API Call"""

        actions = []
        for coroutine in calls:
            if not self._is_call(coroutine) or not coroutine.cr_frame:
                raise TypeError("Coroutine is not an 'Wialon.call' instance")
            coroutine_locals = coroutine.cr_frame.f_locals
            actions.append({
                'svc': convention.prepare_action_name(coroutine_locals['action_name']),
                'params': coroutine_locals['params']
            })
            coroutine.close()
        return await self.core_batch(params=actions, flags=flags_)

    async def multipart(self, call: Coroutine[Any, Any, Any],
                        *fields: MultipartField) -> Any:
        """Adapter method for 'Wialon.call()' coroutine
         to send multipart data to server"""

        if not self._is_call(call) or not call.cr_frame:
            raise TypeError("Coroutine is not an Wialon.call")
        coroutine_locals = call.cr_frame.f_locals
        action_name = coroutine_locals['action_name']
        params = coroutine_locals['params']
        call.close()
        form_data = aiohttp.FormData(
            {
                'sid': self._sid,
                'svc': convention.prepare_action_name(action_name),
                'params': json.dumps(params)
            }
        )
        for f in fields:
            form_data.add_field(**f.dict())
        return await self.request(action_name, self.__base_api_url, payload=form_data)

    @classmethod
    def _is_call(cls, coroutine: Coroutine[Any, Any, Any]) -> bool:
        """Internally check if coroutine is the 'Wialon.call()' method"""

        if coroutine.__qualname__ == cls.call.__qualname__:
            return True
        return False

    def __getattr__(self, action_name: str):
        """
        Enable the calling of Wialon API methods through Python method calls
        of the same name.
        """

        def get(_self, *args, **kwargs):
            return self.call(action_name, *args, **kwargs)

        return get.__get__(self, object)

    async def request(self, action_name: str, url: str, payload: Any) -> Any:
        """
        Base request method for Wialon API Client
        Can be used to perform direct requests for not declared methods,
        but not recommended
        """

        await self.__exclusive_session_lock.wait()

        if not action_name:
            action_name = "undefined_action"
        async with self.__limiter:
            async with self.__semaphore:
                async with aiohttp.ClientSession(
                        trust_env=True,
                        trace_configs=[aiohttp_trace_config],
                        timeout=self._timeout) as session:
                    try:
                        async with session.post(url=url, data=payload) as response:
                            # response.raise_for_status()
                            await WialonCallRespValidator.validate_headers(response)

                            if await WialonCallRespValidator.has_attachment(response):
                                return await response.content.read()

                            response_data = await response.read()
                            result = json.loads(response_data)
                            await WialonCallRespValidator.validate_result(action_name, result)
                            return result
                    except (aiohttp.ClientError, WialonError) as e:
                        logger.exception(e)
                        raise

    async def wait(self, call: Coroutine[Any, Any, Any], timeout: Optional[float] = None) -> Any:
        """Decorate a Call with specified request timeout"""
        prev_timeout = self.timeout
        if timeout:
            self.timeout = timeout
        try:
            return await call
        finally:
            self.timeout = prev_timeout

    @staticmethod
    def help(service_name: str, action_name: str) -> None:
        """
        Open an interactive help for pair if service/action of Wialon Remote API
        Example:
            >>> Wialon.help('core', 'search_item')  # will open the help page
        """

        url = "https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/{service_name}/{action_name}"
        try:
            # pylint: disable=import-outside-toplevel
            import webbrowser
            webbrowser.open(url.format(service_name=service_name, action_name=action_name))
        except ImportError:
            logger.info("Cannot open webbrowser: %s", url)


__all__ = ['Wialon']
