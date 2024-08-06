from typing import Any, Dict

import aiohttp

from aiowialon.exceptions import WIALON_EXCEPTIONS, WialonError, WialonInvalidResult


class WialonCallResponseValidator:

    @staticmethod
    async def raise_wialon_error(action_name: str, result: Dict[str, Any]) -> None:
        code = result.get('error', 6)
        if code == 0:
            return
        reason = result.get("reason", None)
        raise WIALON_EXCEPTIONS[code](action_name, reason)

    @staticmethod
    async def validate_headers(action_name, response: aiohttp.ClientResponse) -> None:
        response_headers = response.headers
        content_type = response_headers.getone('Content-Type')

        if content_type != 'application/json':
            raise WialonInvalidResult(
                reason=f"Invalid response content type: expected 'application/json', got '{content_type}'",
                action_name=action_name
            )

    @staticmethod
    async def validate_result(action_name: str, result: Any) -> None:
        if isinstance(result, dict):
            if 'error' in result:
                await WialonCallResponseValidator.raise_wialon_error(action_name, result)
        if action_name == 'core_batch':
            if isinstance(result, list):
                exceptions = []
                for i, item in enumerate(result):
                    try:
                        await WialonCallResponseValidator.validate_result(str(i), item)
                    except WialonError as err:
                        exceptions.append(f"{i}. {err}")
                if exceptions:
                    reasons = ", ".join(exceptions)
                    raise WialonInvalidResult(f'[{reasons}]', 'core_batch')
