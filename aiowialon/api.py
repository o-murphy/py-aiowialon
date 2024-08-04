#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import inspect
import json
from typing import Callable, Coroutine, Dict, Optional, Any, Union
from typing_extensions import Unpack
from urllib.parse import urljoin

import aiohttp
from aiohttp.client_exceptions import ClientResponseError, ClientConnectorError

from aiowialon.exceptions import WialonError
from aiowialon.types import AvlEventHandler, AvlEventFilter, AvlEvent, AvlEventCallback
from aiowialon.types import LoginParams, OnLoginCallback


class Wialon:
    request_headers: dict = {
        'Accept-Encoding': 'gzip, deflate'
    }

    def __init__(self, scheme: str = 'http', host: str = "hst-api.wialon.com",
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
        self.__on_session_open: Optional[Callable[[], Coroutine]] = None
        self.__task: Optional[asyncio.Task] = None

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

    def on_session_open(self, callback: Optional[OnLoginCallback] = None) -> OnLoginCallback:
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

    def start_poling(self, timeout: Union[int, float] = 2, **params: Unpack[LoginParams]) -> None:
        if not self.__task:
            asyncio.create_task(self.poling(timeout, **params))
        else:
            raise RuntimeError("Wialon Polling Task already started")

    def stop_poling(self) -> None:
        if self.__task:
            self.__task.cancel()
            self.__task = None
        else:
            raise RuntimeError("Wialon Polling Task already stopped")

    async def poling(self, timeout: Union[int, float] = 2, **params: Unpack[LoginParams]) -> None:
        if timeout < 1:
            raise ValueError("Poling timeout have to be >= 1 second. "
                             "No more than 10 “poling” - requests can be processed during 10 seconds")
        await self.login(**params)
        while self.sid:
            response = await self.avl_evts()
            events = AvlEvent.parse_avl_events_response(response)
            await asyncio.gather(*[self.process_event_handlers(event) for event in events])
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

    def batch(self, *calls: Coroutine, flags: int = 0) -> Coroutine[Any, Any, Any]:
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
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=payload, headers=self.request_headers) as response:
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

        if auth_hash:
            session = await self.core_use_auth_hash(**params)
        else:
            if token:
                self.token = token
            params['token'] = self.token
            session = await self.token_login(**params)

        if isinstance(session, dict):
            self.sid = session['eid']
        else:
            raise TypeError(f"Unexpected login response: {session}")
        if self.__on_session_open:
            await self.__on_session_open()
        return session

    def __getattr__(self, action_name: str):
        """
        Enable the calling of Wialon API methods through Python method calls
        of the same name.
        """

        def get(_self, *args, **kwargs):
            return self.call(action_name, *args, **kwargs)

        return get.__get__(self, object)
