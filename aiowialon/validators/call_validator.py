"""Default validator of responses to Wialon Remote API"""

from typing import Any, Dict
import warnings

import aiohttp

from aiowialon.exceptions import WIALON_EXCEPTIONS, WialonError, WialonInvalidResult, WialonWarning


class WialonCallRespValidator:
    """Validator for responses from Wialon Remote API"""

    @staticmethod
    async def raise_wialon_error(action_name: str, result: Dict[str, Any]) -> None:
        """
        Extracts the error code and reason from error message returned from Wialon Remote API,
        Raises specific exception, depending on response result
        """

        code = result.get('error', 6)
        if code == 0:
            return
        reason = result.get("reason", None)
        if code in WIALON_EXCEPTIONS:
            raise WIALON_EXCEPTIONS[code](reason, action_name, result)
        if code in WialonError.errors:
            raise WialonError(code, reason, action_name, result)

    @staticmethod
    async def validate_headers(response: aiohttp.ClientResponse) -> None:
        """Checks the response headers, raises Warnings if got unexpected data type"""

        content_type = response.headers.get('Content-Type', None)

        if not content_type:
            warnings.warn(f"Cant recognize content type: {response.headers}",
                          WialonWarning)
        elif content_type != 'application/json':
            warnings.warn(f"Invalid response content type, "
                          f"expected 'application/json', "
                          f" '{response.headers.get('Content-Type')}'",
                          WialonWarning)
            # # Fixme: this part not tested, so can pass some unexpected responses
            # raise WialonInvalidResult(
            #     f"Invalid response content type: "
            #     f"expected 'application/json', got '{content_type}'",
            #     action_name,
            #     await response.read()
            # )

    @staticmethod
    async def validate_result(action_name: str, result: Any) -> None:
        """
        Validates result of response depend on its type,
        action and error code,
        Recursively validates 'core_batch request' results
        """
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

    @staticmethod
    async def has_attachment(response: aiohttp.ClientResponse) -> bool:
        """
        Check if response has a binary attachment
        """
        content_type = response.headers.get('Content-Type', '').lower()
        content_disposition = response.headers.get('Content-Disposition')
        if content_disposition and 'attachment' in content_disposition.lower():
            # # Fixme: working as expected, but maybe will have adjustments
            # match = re.search(r'filename="(.+)"', content_disposition)
            # if match:
            #     return True
            return True
        if 'application/octet-stream' in content_type or 'multipart/form-data' in content_type:
            return True
        return False


__all__ = ['WialonCallRespValidator']
