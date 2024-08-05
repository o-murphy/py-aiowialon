from typing import Any

import aiohttp

from aiowialon.exceptions import WialonError


class CallResponseValidator:

    @staticmethod
    async def validate_result(action_name: str, result: Any) -> None:
        if isinstance(result, dict) and 'error' in result and result.get('error', 6) > 0:
            raise WialonError(
                code=result.get("error", 6),
                reason=result.get("reason", ""),
                action_name=action_name
            )

    @staticmethod
    async def validate_batch_result(result: Any):
        if isinstance(result, list):
            exceptions = []
            # Check for batch errors
            for i, item in enumerate(result):
                try:
                    if isinstance(item, dict) and 'error' in item and item.get('error', 6) > 0:
                        raise WialonError(code=item.get("error", 6), reason=item.get("reason", ""))
                except WialonError as e:
                    exceptions.append(f"{i}. {e}")

            if exceptions:
                reasons = ", ".join(exceptions)
                raise WialonError(3, f'[{reasons}]', 'core_batch')

    @staticmethod
    async def validate_headers(action_name, response: aiohttp.ClientResponse) -> None:
        response_headers = response.headers
        content_type = response_headers.getone('Content-Type')

        if content_type != 'application/json':
            raise WialonError(
                code=3,
                reason=f"Invalid response content type",
                action_name=action_name
            )
