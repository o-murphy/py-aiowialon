from typing import Any, Dict

import aiohttp

from aiowialon.exceptions import WIALON_EXCEPTIONS, WialonError, WialonInvalidResult


class WialonCallRespValidator:

    @staticmethod
    async def raise_wialon_error(action_name: str, result: Dict[str, Any]) -> None:
        code = result.get('error', 6)
        if code == 0:
            return
        reason = result.get("reason", None)
        if code in WIALON_EXCEPTIONS:
            raise WIALON_EXCEPTIONS[code](reason, action_name, result)
        if code in WialonError.errors:
            raise WialonError(code, reason, action_name, result)

    @staticmethod
    async def validate_headers(action_name, response: aiohttp.ClientResponse) -> None:
        response_headers = response.headers
        content_type = response_headers.getone('Content-Type')

        if content_type != 'application/json':
            raise WialonInvalidResult(
                f"Invalid response content type: "
                f"expected 'application/json', got '{content_type}'",
                action_name,
                await response.read()
            )

    @staticmethod
    async def validate_result(action_name: str, result: Any) -> None:
        if isinstance(result, dict):
            if 'error' in result:
                await WialonCallRespValidator.raise_wialon_error(action_name, result)
        if action_name == 'core_batch':
            if isinstance(result, list):
                exceptions = []
                for i, item in enumerate(result):
                    try:
                        await WialonCallRespValidator.validate_result(f"core_batch[{i}]", item)
                    except WialonError as err:
                        exceptions.append(err)
                if len(exceptions) > 0:
                    raise WialonInvalidResult(exceptions, 'core_batch', result)


__all__ = ['WialonCallRespValidator']
