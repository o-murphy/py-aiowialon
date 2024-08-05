import logging

import aiohttp

logger = logging.getLogger('aiowialon')
logger.setLevel(logging.INFO)

aiohttp_client_logger = logging.getLogger('aiohttp.client')


async def on_request_start(session, context, params) -> None:
    aiohttp_client_logger.debug(f"Request started: {params.method} {params.url}")


async def on_request_end(session, context, params) -> None:
    aiohttp_client_logger.debug(f"Request ended: {params.method} {params.url}")


async def on_request_exception(session, context, params) -> None:
    aiohttp_client_logger.error(f"Request error: {params.method} {params.url}")


aiohttp_trace_config = aiohttp.TraceConfig()
aiohttp_trace_config.on_request_start.append(on_request_start)
aiohttp_trace_config.on_request_end.append(on_request_end)
aiohttp_trace_config.on_request_exception.append(on_request_exception)
