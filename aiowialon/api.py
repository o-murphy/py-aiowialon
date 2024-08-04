#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import json
import logging
from contextlib import suppress
from typing import Callable, Coroutine, Dict, Optional, Any, Union, Literal
from aiowialon.compatibility import Unpack
from urllib.parse import urljoin

import aiohttp
from aiohttp.client_exceptions import ClientResponseError, ClientConnectorError

from aiowialon.exceptions import WialonError
from aiowialon.logger import logger, aiohttp_client_logger
from aiowialon.types import AvlEventHandler, AvlEventFilter, AvlEvent, AvlEventCallback
from aiowialon.types import LoginParams, OnLoginCallback
from aiowialon.types.flags import BatchFlag


class Wialon:
    request_headers: dict = {
        'Accept-Encoding': 'gzip, deflate'
    }

    def __init__(self, scheme: Literal['https', 'http'] = 'http', host: str = "hst-api.wialon.com",
                 port: int = 80, token: Optional[str] = None, sid: Optional[str] = None, **extra_params: Dict):
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
        self._running_lock = asyncio.Lock()

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

    def event_handler(self, filter_: Optional[AvlEventFilter] = None) -> Callable:
        def decorator(callback: AvlEventCallback):
            handler = AvlEventHandler(callback, filter_)
            if callback.__name__ in self.__handlers:
                raise KeyError(f"Detected EventHandler duplicate {callback.__name__}")
            self.__handlers[callback.__name__] = handler
            return callback

        return decorator

    async def process_event_handlers(self, event: AvlEvent) -> None:
        for name, handler in self.__handlers.items():
            if await handler(event):
                break

    async def start_polling(self, timeout: Union[int, float] = 2, **params: Unpack[LoginParams]) -> None:
        async with self._running_lock:

            try:
                tasks = [
                    asyncio.create_task(self._polling(timeout, **params)),
                ]
                done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                for task in pending:
                    task.cancel()
                    with suppress(asyncio.CancelledError):
                        await task
                await asyncio.gather(*done)
            finally:
                try:
                    await self.stop_polling()
                finally:
                    logger.info("Polling stopped")

    async def stop_polling(self) -> Any:
        """
        Execute this method if you want to stop polling programmatically

        :return:
        """
        if not self._running_lock.locked():
            raise RuntimeError("Polling is not started")
        if self.sid:
            logout = await self.core_logout()
            self.sid = None
            return logout

    async def _polling(self, timeout: Union[int, float] = 2, **params: Unpack[LoginParams]) -> None:
        if timeout < 1:
            raise ValueError("Poling timeout have to be >= 1 second. "
                             "No more than 10 “poling” - requests can be processed during 10 seconds")
        try:
            await self.login(**params)
        except WialonError as e:
            logger.exception(e)
            return

        while self.sid:
            response = await self.avl_evts()
            events = AvlEvent.parse_avl_events_response(response)
            try:
                await asyncio.gather(*[self.process_event_handlers(event) for event in events])
            except WialonError as err:
                if err._code == 1003:
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

        params = self._prepare_params(params)
        payload = json.dumps(params, ensure_ascii=False)
        params = {
            'svc': self._prepare_action_name(action_name),
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
    def _prepare_action_name(action_name: str) -> str:
        return action_name.replace('_', '/', 1)

    @classmethod
    def _prepare_params(cls, params: dict) -> dict:
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
                new_params[new_key] = cls._prepare_params(v)
            elif isinstance(v, list):
                new_params[new_key] = [cls._prepare_params(item) if isinstance(item, dict) else item for
                                       item in v]
            else:
                new_params[new_key] = v
        return new_params

    def batch(self, *calls: Coroutine, flags: BatchFlag = BatchFlag.EXECUTE_ALL) -> Coroutine[Any, Any, Any]:
        actions = []

        for coroutine in calls:
            if not self._is_call(coroutine) or not coroutine.cr_frame:
                raise TypeError("Coroutine is not an Wialon.call")
            coroutine_locals = coroutine.cr_frame.f_locals
            actions.append({
                'svc': self._prepare_action_name(coroutine_locals['action_name']),
                'params': coroutine_locals['params']
            })
            coroutine.close()

        batch_params = {
            'params': actions,
            'flags': flags
        }
        return self.core_batch(**batch_params)

    async def request(self, action_name: str, url: str, payload: Any) -> Any:
        async def on_request_start(session, context, params):
            logging.getLogger('aiohttp.client').debug(f'<{params}>')

        try:

            async def on_request_start(session, context, params):
                aiohttp_client_logger.debug(f'<{params}>')

            async def on_request_end(session, context, params):
                aiohttp_client_logger.debug(f'<{params}>')

            # async def on_response_chunk_received(session, context, params):
            #     aiohttp_client_logger.debug(f'<{params}>')

            trace_config = aiohttp.TraceConfig()
            trace_config.on_request_start.append(on_request_start)
            trace_config.on_request_end.append(on_request_end)
            # trace_config.on_response_chunk_received.append(on_response_chunk_received)

            async with aiohttp.ClientSession(trace_configs=[trace_config]) as session:
                async with session.post(url, data=payload, headers=self.request_headers, ) as response:
                    response_data = await response.read()
                    response_headers = response.headers
                    content_type = response_headers.getone('Content-Type')

                    try:
                        if content_type == 'application/json':
                            result = json.loads(response_data)
                    except ValueError as e:
                        raise WialonError(
                            0,
                            f"Invalid response from Wialon: {e}",
                        )

                    if isinstance(result, dict) and 'error' in result and result['error'] > 0:
                        raise WialonError(result['error'], action_name)

                    errors = []
                    if isinstance(result, list):
                        # Check for batch errors
                        for elem in result:
                            if not isinstance(elem, dict):
                                continue
                            if "error" in elem:
                                errors.append("%s (%d)" % (WialonError.errors[elem["error"]], elem["error"]))

                    if errors:
                        errors.append(action_name)
                        raise WialonError(0, " ".join(errors))

                    return result
        except ClientResponseError as e:
            raise WialonError(0, f"HTTP {e.status}")
        except ClientConnectorError as e:
            raise WialonError(0, str(e))
        except Exception as err:
            raise err from err

    async def login(self, **params: Unpack[LoginParams]) -> Dict[str, Any]:
        token = params.get("token", None)
        auth_hash = params.get("auth_hash", None)
        if token and auth_hash:
            raise WialonError(1, "You can't use both token and auth_hash at the login")

        logger.info('Wialon login')
        if auth_hash:
            session = await self.core_use_auth_hash(**params)
        else:
            if token:
                self.token = token
            params['token'] = self.token
            session = await self.token_login(**params)

        if isinstance(session, dict):
            self.sid = session['eid']
            logger.debug(f"sid: {self.sid}")
        else:
            raise TypeError(f"Unexpected login response: {session}")
        if self.__on_session_open:
            await self.__on_session_open(session)
        return session

    def __getattr__(self, action_name: str):
        """
        Enable the calling of Wialon API methods through Python method calls
        of the same name.
        """

        def get(_self, *args, **kwargs):
            return self.call(action_name, *args, **kwargs)

        return get.__get__(self, object)
