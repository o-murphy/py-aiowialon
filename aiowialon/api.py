#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import json
from contextlib import suppress
from typing import Callable, Coroutine, Dict, Optional, Any, Union, Literal
from aiowialon.utils.compatibility import Unpack
from urllib.parse import urljoin

import aiohttp
from aiolimiter import AsyncLimiter

from aiowialon.exceptions import WialonError
from aiowialon.logger import logger, aiohttp_client_logger, aiohttp_trace_config
from aiowialon.types import AvlEventHandler, AvlEventFilter, AvlEvent, AvlEventCallback, OnLogoutCallback
from aiowialon.types import LoginParams, OnLoginCallback
from aiowialon.types.flags import BatchFlag


class Wialon:
    request_headers: dict = {
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    def __init__(self, scheme: Literal['https', 'http'] = 'http', host: str = "hst-api.wialon.com",
                 port: int = 80, token: Optional[str] = None, sid: Optional[str] = None,
                 requests_per_second: int = 10,
                 **extra_params: Any):
        """
        Created the Wialon API object.
        """
        self._sid: Optional[str] = sid
        self._token: Optional[str] = token
        self.__default_params: Dict = {}
        self.__default_params.update(extra_params)

        self.__base_url = f'{scheme}://{host}:{port}'

        self.__base_api_url: str = urljoin(self.__base_url, 'wialon/ajax.html?')

        self.__handlers: Dict[str, AvlEventHandler] = {}
        self.__on_session_open: Optional[OnLoginCallback] = None
        self.__on_session_close: Optional[OnLogoutCallback] = None

        self.__running_lock = asyncio.Lock()
        self.__polling_task: Optional[asyncio.Task] = None

        self.__semaphore = asyncio.Semaphore(10)
        self.__limiter: AsyncLimiter = AsyncLimiter(requests_per_second, 1)

    @property
    def sid(self) -> Optional[str]:
        return self._sid

    @sid.setter
    def sid(self, eid: str) -> None:
        self._sid = eid

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
        self.__default_params.update(params)

    def on_session_open(self, callback: Optional[OnLoginCallback] = None) -> Optional[OnLoginCallback]:
        if callback and not callable(callback):
            raise TypeError("on_session_open callback must be callable")
        self.__on_session_open = callback
        return callback

    def on_session_close(self, callback: Optional[OnLogoutCallback] = None) -> Optional[OnLogoutCallback]:
        if callback and not callable(callback):
            raise TypeError("on_session_open callback must be callable")
        self.__on_session_close = callback
        return callback

    def avl_event_handler(self, filter_: Optional[AvlEventFilter] = None) -> Callable:
        def decorator(callback: AvlEventCallback):
            handler = AvlEventHandler(callback, filter_)
            if callback.__name__ in self.__handlers:
                raise KeyError(f"Detected EventHandler duplicate {callback.__name__}")
            self.__handlers[callback.__name__] = handler
            return callback

        return decorator

    async def _process_event_handlers(self, event: AvlEvent) -> None:
        for name, handler in self.__handlers.items():
            if await handler(event):
                break

    async def start_polling(self, timeout: Union[int, float] = 2,
                            logout_finally: bool = False,
                            **params: Unpack[LoginParams]) -> None:
        if timeout < 1:
            raise ValueError("Poling timeout have to be >= 1 second. "
                             "No more than 10 “poling” - requests can be processed during 10 seconds")

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
            raise ValueError("You can't use both token and auth_hash at the login")

        logger.info('Wialon login')
        if auth_hash:
            session_login = await self.core_use_auth_hash(**params)
        else:
            if token:
                self.token = token
            params['token'] = self.token
            session_login = await self.token_login(**params)

        if isinstance(session_login, dict):
            self.sid = session_login['eid']
            logger.debug(f"sid: {self.sid}")
            logger.info("Wialon session opened")
        else:
            raise TypeError(f"Unexpected login response: {session_login}")
        if self.__on_session_open:
            await self.__on_session_open(session_login)
        return session_login

    async def logout(self) -> Any:
        if self.sid:
            logger.info("Wialon logout")
            session_logout = await self.core_logout()
            self.sid = None
            if self.__on_session_close:
                await self.__on_session_close(session_logout)
            return session_logout

    async def _polling(self, timeout: Union[int, float] = 2) -> None:
        while self.sid:
            try:
                response = await self.avl_evts()
                events = AvlEvent.parse_avl_events_response(response)
                await asyncio.gather(*[self._process_event_handlers(event) for event in events])
            except WialonError as err:
                if err.code == 1003:
                    logger.exception(err)
            await asyncio.sleep(timeout)

    def avl_evts(self) -> Coroutine[Any, Any, Any]:
        """
        Call avl_event request
        """
        url = urljoin(self.__base_url, 'avl_evts')
        params = {
            'sid': self.sid
        }

        return self.request('avl_evts', url, params)

    async def call(self, action_name: str, *args: Any, **params: Any) -> Coroutine[Any, Any, Any]:
        """
        Call the API method provided with the parameters supplied.
        """
        params = self.prepare_params(params)
        payload = json.dumps(params, ensure_ascii=False)
        params = {
            'svc': self.prepare_action_name(action_name),
            'params': payload,
            'sid': self.sid
        }

        full_payload = self.__default_params.copy()
        full_payload.update(params)
        return await self.request(action_name, self.__base_api_url, full_payload)

    @classmethod
    def _is_call(cls, coroutine: Coroutine[Any, Any, Any]) -> bool:
        if coroutine.__qualname__ == cls.call.__qualname__:
            return True
        return False

    @staticmethod
    def prepare_action_name(action_name: str) -> str:
        return action_name.replace('_', '/', 1)

    @staticmethod
    def prepare_params(params: dict) -> dict:
        if not isinstance(params, dict):
            return params

        new_params: Dict[str, Any] = {}
        for k, v in params.items():
            # Remove trailing underscores
            new_key = k.rstrip('_') if k.endswith('_') else k

            # Convert CapitalisedKey to capitalisedParam
            new_key = new_key[:1].lower() + new_key[1:] if new_key else ''

            # Process nested dictionaries and lists
            if isinstance(v, dict):
                new_params[new_key] = Wialon.prepare_params(v)
            elif isinstance(v, list):
                new_params[new_key] = [Wialon.prepare_params(item) if isinstance(item, dict) else item for
                                       item in v]
            else:
                new_params[new_key] = v
        return new_params

    def batch(self, *calls: Coroutine[Any, Any, Any],
              flags: BatchFlag = BatchFlag.EXECUTE_ALL) -> Coroutine[Any, Any, Any]:
        actions = []
        for coroutine in calls:
            if not self._is_call(coroutine) or not coroutine.cr_frame:
                raise TypeError("Coroutine is not an Wialon.call")
            coroutine_locals = coroutine.cr_frame.f_locals
            actions.append({
                'svc': self.prepare_action_name(coroutine_locals['action_name']),
                'params': coroutine_locals['params']
            })
            coroutine.close()
        return self.core_batch(params=actions, flags=flags)

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
                        async with session.post(url, data=payload, headers=self.request_headers) as response:
                            response_data = await response.read()
                            response_headers = response.headers
                            content_type = response_headers.getone('Content-Type')

                            try:
                                if content_type == 'application/json':
                                    result = json.loads(response_data)
                            except ValueError as e:
                                raise WialonError(
                                    code=3,
                                    reason=f"Invalid response content type",
                                    action_name=action_name
                                )

                            if isinstance(result, dict) and 'error' in result and result.get('error', 6) > 0:
                                raise WialonError(
                                    code=result.get("error", 6),
                                    reason=result.get("reason", ""),
                                    action_name=action_name
                                )

                            if isinstance(result, list) and action_name == 'core_batch':
                                errors = []
                                # Check for batch errors
                                for i, item in enumerate(result):
                                    if isinstance(item, dict) and 'error' in item and item.get('error', 6) > 0:
                                        err = WialonError(code=item.get("error", 6), reason=item.get("reason", ""))
                                        errors.append(f"{i}. {err.description()}")

                                if errors:
                                    reasons = ", ".join(errors)
                                    raise WialonError(3, f'[{reasons}]', action_name)

                            return result
                    except Exception as e:
                        logger.exception(e)
                        raise

    @staticmethod
    def help(service_name: str, action_name: str) -> None:
        url = f"https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/{service_name}/{action_name}"
        try:
            import webbrowser
            webbrowser.open(url)
        except Exception as e:
            logger.info(f"Cannot open webbrowser: {url}")
