#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import json
from typing import Callable, Coroutine, Dict, Optional, Any
from urllib.parse import urljoin

import aiohttp
from aiohttp.client_exceptions import ClientResponseError, ClientConnectorError

from aiowialon.exceptions import WialonError
from aiowialon.types.event import AvlEventHandler, AvlEventFilter, AvlEvent


class Wialon:
    request_headers: dict = {
        'Accept-Encoding': 'gzip, deflate'
    }

    def __init__(self, scheme: str = 'http', host: str = "hst-api.wialon.com",
                 port: int = 80, token: str = None, sid: str = None, **extra_params: Any):
        """
        Created the Wialon API object.
        """
        self._sid: str = sid
        self._token: str = token
        self.__default_params: Dict = {}
        self.__default_params.update(extra_params)

        self.__base_url = f'{scheme}://{host}:{port}'

        self.__base_api_url: str = urljoin(self.__base_url, 'wialon/ajax.html?')

        self.__handlers: Dict[str, AvlEventHandler] = {}
        self.__on_session_open: Optional[Callable[[], Coroutine]] = None
        self.__task: Optional[asyncio.Task] = None

    @property
    def sid(self) -> str:
        return self._sid

    @sid.setter
    def sid(self, eid: str) -> None:
        self._sid = eid

    @property
    def token(self) -> str:
        return self._token

    @token.setter
    def token(self, token: str) -> None:
        self._token = token

    def update_extra_params(self, **params: Any) -> None:
        """
        Updated the Wialon API default parameters.
        """
        self.__default_params.update(params)

    def on_session_open(self, callback: Optional[Callable[[], Coroutine]] = None) -> Callable:
        if callback and not callable(callback):
            raise TypeError("on_session_open callback must be callable")
        self.__on_session_open = callback
        return callback

    def event_handler(self, filter_: AvlEventFilter = None) -> Callable:
        def decorator(callback: AvlEventHandler):
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

    def start_poling(self, token: str = None, timeout: [int, float] = 2) -> None:
        if not self.__task:
            asyncio.create_task(self.poling(token, timeout))
        else:
            raise RuntimeError("Wialon Polling Task already started")

    def stop_poling(self) -> None:
        if self.__task:
            self.__task.cancel()
            self.__task = None
        else:
            raise RuntimeError("Wialon Polling Task already stopped")

    async def poling(self, token: str = None, timeout: [float, int] = 2) -> None:
        if timeout < 1:
            raise ValueError("Poling timeout have to be >= 1 second. "
                             "No more than 10 “poling” - requests can be processed during 10 seconds")
        await self.token_login(token=token)
        while self.sid:
            response = await self.avl_evts()
            events = AvlEvent.parse_avl_events_response(response)
            await asyncio.gather(*[self.process_event_handlers(event) for event in events])
            await asyncio.sleep(timeout)

    async def avl_evts(self) -> Coroutine[Any, Any, None]:
        """
        Call avl_event request
        """
        url = urljoin(self.__base_url, 'avl_evts')
        params = {
            'sid': self.sid
        }

        return await self.request('avl_evts', url, params)

    async def call(self, action_name: str, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]:
        """
        Call the API method provided with the parameters supplied.
        """

        def replace_keys_and_convert_format(d):
            if not isinstance(d, dict):
                return d

            new_dict = {}
            for k, v in d.items():
                # Remove trailing underscores
                new_key = k.rstrip('_') if k.endswith('_') else k

                # Convert CapitalisedKey to capitalisedParam
                new_key = new_key[:1].lower() + new_key[1:] if new_key else ''

                # Process nested dictionaries and lists
                if isinstance(v, dict):
                    new_dict[new_key] = replace_keys_and_convert_format(v)
                elif isinstance(v, list):
                    new_dict[new_key] = [replace_keys_and_convert_format(item) if isinstance(item, dict) else item for
                                         item in v]
                else:
                    new_dict[new_key] = v
            return new_dict

        kwargs = replace_keys_and_convert_format(kwargs)

        if not kwargs:
            # List params for batch
            if isinstance(args, tuple) and len(args) == 1:
                params = json.dumps(args[0], ensure_ascii=False)
            else:
                params = json.dumps(args, ensure_ascii=False)
        else:
            params = json.dumps(kwargs, ensure_ascii=False)

        params = {
            'svc': action_name.replace('_', '/', 1),
            'params': params,
            'sid': self.sid
        }

        all_params = self.__default_params.copy()
        all_params.update(params)
        return await self.request(action_name, self.__base_api_url, all_params)

    async def token_login(self, token: str = None, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]:
        if token:
            self.token = token
        kwargs['token'] = self.token
        kwargs['appName'] = 'py-aiowialon'
        sess = await self.call('token_login', *args, **kwargs)
        if sess:
            self.sid = sess['eid']
        if self.__on_session_open:
            await self.__on_session_open()
        return sess

    async def request(self, action_name: str, url: str, payload: Any) -> Coroutine[Any, Any, None]:
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

    def __getattr__(self, action_name: str):
        """
        Enable the calling of Wialon API methods through Python method calls
        of the same name.
        """

        def get(_self, *args, **kwargs):
            return self.call(action_name, *args, **kwargs)

        return get.__get__(self, object)
