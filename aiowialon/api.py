#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import json
from contextlib import suppress
from typing import Callable, Coroutine, Dict, Optional, Any, Union, Literal, List
from urllib.parse import urljoin

import aiohttp
from aiolimiter import AsyncLimiter

from aiowialon.exceptions import WialonError, WialonRequestLimitExceededError
from aiowialon.logger import logger, aiohttp_trace_config
from aiowialon.types import (AvlEventHandler, AvlEventFilter, AvlEvent,
                             AvlEventCallback, LogoutCallback)
from aiowialon.types import LoginParams, LoginCallback
from aiowialon.types import flags
from aiowialon.utils import convention
from aiowialon.utils.compat import Unpack
from aiowialon.validators import WialonCallRespValidator


# pylint: disable=too-many-instance-attributes
class Wialon:
    request_headers: dict = {
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # pylint: disable=too-many-arguments
    def __init__(self, scheme: Literal['https', 'http'] = 'https',
                 host: str = "hst-api.wialon.com", port: Optional[int] = None,
                 token: Optional[str] = None,
                 requests_per_second: int = 10,
                 **extra_params: Any):
        """
        Creates the Wialon API client.
        """

        self._sid: Optional[str] = None
        self._token: Optional[str] = token
        self._default_params: Dict = {}
        self._default_params.update(extra_params)

        self.__base_url = f"{scheme}://{host}:{port if port else 443 if scheme == 'https' else 80}"
        self.__base_api_url: str = urljoin(self.__base_url, 'wialon/ajax.html')

        self.__handlers: Dict[str, AvlEventHandler] = {}
        self.__on_session_open: Optional[LoginCallback] = None
        self.__on_session_close: Optional[LogoutCallback] = None

        self.__running_lock = asyncio.Lock()
        self.__polling_task: Optional[asyncio.Task] = None

        self.__semaphore = asyncio.Semaphore(10)
        self.__limiter: AsyncLimiter = AsyncLimiter(requests_per_second, 1)

    @property
    def token(self) -> Optional[str]:
        return self._token

    @token.setter
    def token(self, token: str) -> None:
        self._token = token

    def update_extra_params(self, **params: Any) -> None:
        """
        Updated the Wialon API default parameters.
        """
        self._default_params.update(params)

    def on_session_open(self,
                        callback: Optional[LoginCallback] = None) -> Optional[LoginCallback]:
        if callback and not callable(callback):
            raise TypeError(f"'on_session_open' callback must be a type of {LoginCallback}")
        self.__on_session_open = callback
        return callback

    def on_session_close(self,
                         callback: Optional[LogoutCallback] = None) -> Optional[LogoutCallback]:
        if callback and not callable(callback):
            raise TypeError(f"'on_session_close' callback must be a type of {LogoutCallback}")
        self.__on_session_close = callback
        return callback

    def avl_event_handler(self, filter_: Optional[AvlEventFilter] = None) -> Callable:
        def wrapper(callback: AvlEventCallback):
            handler = AvlEventHandler(callback, filter_)
            if callback.__name__ in self.__handlers:
                raise KeyError(f"Detected EventHandler duplicate {callback.__name__}")
            self.__handlers[callback.__name__] = handler
            return callback
        return wrapper

    async def _process_event_handlers(self, event: AvlEvent) -> None:
        for _, handler in self.__handlers.items():
            if await handler(event):
                break

    async def start_polling(self, timeout: Union[int, float] = 2,
                            logout_finally: bool = False,
                            **params: Unpack[LoginParams]) -> None:
        if timeout < 1:
            raise ValueError("Poling timeout have to be >= 1 second. "
                             "No more than 10 'avl_evts' requests "
                             "can be processed during 10 seconds")

        async with self.__running_lock:

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
        """
        Execute this method if you want to stop polling programmatically
        :return:
        """
        if not self.__running_lock.locked():
            raise RuntimeError("Polling is not started")

        if self.__polling_task:
            logger.info("Stopping polling task")
            self.__polling_task.cancel()
            with suppress(asyncio.CancelledError):
                await self.__polling_task
            self.__polling_task = None
        if logout:
            await self.logout()

    async def login(self, **params: Unpack[LoginParams]) -> Dict[str, Any]:
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
        if self._sid:
            logger.info("Wialon logout")
            session_logout = await self.core_logout()
            self._sid = None
            if self.__on_session_close:
                await self.__on_session_close(session_logout)
            return session_logout

    async def _polling(self, timeout: Union[int, float] = 2) -> None:
        while self._sid:
            try:
                response = await self.avl_evts()
                events = AvlEvent.parse_avl_events_response(response)
                await asyncio.gather(*[self._process_event_handlers(event) for event in events])
            except WialonRequestLimitExceededError as err:
                logger.exception(err)
            await asyncio.sleep(timeout)

    async def avl_evts(self) -> Any:
        """
        Call avl_event request
        """
        url = urljoin(self.__base_url, 'avl_evts')
        params = {
            'sid': self._sid
        }

        return await self.request('avl_evts', url, params)

    # pylint: disable=unused-argument
    async def call(self, action_name: str, *args: Any, **params: Any) -> Any:
        """
        Call the API method provided with the parameters supplied.
        """
        params = convention.prepare_action_params(params)
        payload = json.dumps(params, ensure_ascii=False)
        params = {
            'svc': convention.prepare_action_name(action_name),
            'params': payload,
            'sid': self._sid
        }

        full_payload = self._default_params.copy()
        full_payload.update(params)
        return await self.request(action_name, self.__base_api_url, full_payload)

    @classmethod
    def _is_call(cls, coroutine: Coroutine[Any, Any, Any]) -> bool:
        if coroutine.__qualname__ == cls.call.__qualname__:
            return True
        return False

    async def batch(self, *calls: Coroutine[Any, Any, Any],
                    flags_: flags.BatchFlag = flags.BatchFlag.EXECUTE_ALL) -> List[Any]:
        actions = []
        for coroutine in calls:
            if not self._is_call(coroutine) or not coroutine.cr_frame:
                raise TypeError("Coroutine is not an Wialon.call")
            coroutine_locals = coroutine.cr_frame.f_locals
            actions.append({
                'svc': convention.prepare_action_name(coroutine_locals['action_name']),
                'params': coroutine_locals['params']
            })
            coroutine.close()
        return await self.core_batch(params=actions, flags=flags_)

    def __getattr__(self, action_name: str):
        """
        Enable the calling of Wialon API methods through Python method calls
        of the same name.
        """

        def get(_self, *args, **kwargs):
            return self.call(action_name, *args, **kwargs)

        return get.__get__(self, object)

    async def request(self, action_name: str, url: str, payload: Any) -> Any:
        async with self.__limiter:
            async with self.__semaphore:
                async with aiohttp.ClientSession(
                        trust_env=True,
                        trace_configs=[aiohttp_trace_config]) as session:
                    try:
                        async with session.post(
                                url=url,
                                data=payload,
                                headers=self.request_headers) as response:
                            response_data = await response.read()
                            await WialonCallRespValidator.validate_headers(action_name, response)
                            result = json.loads(response_data)
                            await WialonCallRespValidator.validate_result(action_name, result)
                            return result
                    except (aiohttp.ClientError, WialonError) as e:
                        logger.exception(e)
                        raise

    @staticmethod
    def help(service_name: str, action_name: str) -> None:
        url = "https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/{service_name}/{action_name}"
        try:
            # pylint: disable=import-outside-toplevel
            import webbrowser
            webbrowser.open(url.format(service_name=service_name, action_name=action_name))
        except ImportError:
            logger.info("Cannot open webbrowser: %s", url)


__all__ = ['Wialon']
