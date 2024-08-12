"""Definitions of logging settings for aiowialon debug."""

import logging

import aiohttp

logger = logging.getLogger('aiowialon')
logger.setLevel(logging.INFO)

aiohttp_client_logger = logging.getLogger('aiohttp.client')


# pylint: disable=unused-argument
async def on_request_start(session, context, params) -> None:
    """aiohttp.ClientSession logging on_request_start callback"""
    aiohttp_client_logger.debug("Request started: %s %s", params.method, params.url)


# pylint: disable=unused-argument
async def on_request_end(session, context, params) -> None:
    """aiohttp.ClientSession logging on_request_end callback"""
    aiohttp_client_logger.debug("Request ended: %s %s", params.method, params.url)


# pylint: disable=unused-argument
async def on_request_exception(session, context, params) -> None:
    """aiohttp.ClientSession logging on_request_exception callback"""
    aiohttp_client_logger.error("Request error: %s %s", params.method, params.url)


aiohttp_trace_config = aiohttp.TraceConfig()
aiohttp_trace_config.on_request_start.append(on_request_start)
aiohttp_trace_config.on_request_end.append(on_request_end)
aiohttp_trace_config.on_request_exception.append(on_request_exception)

__all__ = (
    'logger',
    'aiohttp_trace_config',
)
