"""Tests for WialonCallRespValidator"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from aiowialon.validators.call_validator import WialonCallRespValidator
from aiowialon.exceptions import (
    WialonError,
    WialonInvalidSession,
    WialonAccessDenied,
    WialonInvalidResult,
    WialonRequestLimitExceededError,
)


# ---------------------------------------------------------------------------
# raise_wialon_error
# ---------------------------------------------------------------------------

class TestRaiseWialonError:
    @pytest.mark.asyncio
    async def test_code_zero_does_not_raise(self):
        await WialonCallRespValidator.raise_wialon_error("action", {"error": 0})

    @pytest.mark.asyncio
    async def test_known_code_raises_specific_exception(self):
        with pytest.raises(WialonInvalidSession):
            await WialonCallRespValidator.raise_wialon_error("a", {"error": 1})

    @pytest.mark.asyncio
    async def test_access_denied_raises(self):
        with pytest.raises(WialonAccessDenied):
            await WialonCallRespValidator.raise_wialon_error("a", {"error": 7})

    @pytest.mark.asyncio
    async def test_unknown_code_raises_base_wialon_error(self):
        with pytest.raises(WialonError) as exc_info:
            await WialonCallRespValidator.raise_wialon_error("a", {"error": 9999})
        assert exc_info.value.code == 9999

    @pytest.mark.asyncio
    async def test_reason_passed_to_exception(self):
        with pytest.raises(WialonError) as exc_info:
            await WialonCallRespValidator.raise_wialon_error(
                "a", {"error": 4, "reason": "bad param"}
            )
        assert exc_info.value.reason == "bad param"

    @pytest.mark.asyncio
    async def test_action_name_passed_to_exception(self):
        with pytest.raises(WialonError) as exc_info:
            await WialonCallRespValidator.raise_wialon_error(
                "core_search_item", {"error": 7}
            )
        assert exc_info.value.action_name == "core_search_item"

    @pytest.mark.asyncio
    async def test_missing_error_key_defaults_to_6(self):
        # error key missing → code defaults to 6 (unknown)
        with pytest.raises(WialonError) as exc_info:
            await WialonCallRespValidator.raise_wialon_error("a", {})
        assert exc_info.value.code == 6


# ---------------------------------------------------------------------------
# validate_result
# ---------------------------------------------------------------------------

class TestValidateResult:
    @pytest.mark.asyncio
    async def test_dict_without_error_key_passes(self):
        await WialonCallRespValidator.validate_result("action", {"items": []})

    @pytest.mark.asyncio
    async def test_dict_with_error_zero_passes(self):
        await WialonCallRespValidator.validate_result("action", {"error": 0})

    @pytest.mark.asyncio
    async def test_dict_with_error_raises(self):
        with pytest.raises(WialonError):
            await WialonCallRespValidator.validate_result("action", {"error": 7})

    @pytest.mark.asyncio
    async def test_list_result_for_non_batch_passes(self):
        await WialonCallRespValidator.validate_result("core_search_items", [1, 2, 3])

    @pytest.mark.asyncio
    async def test_core_batch_all_ok(self):
        result = [{"items": []}, {"items": []}]
        await WialonCallRespValidator.validate_result("core_batch", result)

    @pytest.mark.asyncio
    async def test_core_batch_partial_error_raises_invalid_result(self):
        result = [{"error": 0}, {"error": 7}]
        with pytest.raises(WialonInvalidResult) as exc_info:
            await WialonCallRespValidator.validate_result("core_batch", result)
        assert isinstance(exc_info.value.reason, list)
        assert len(exc_info.value.reason) == 1

    @pytest.mark.asyncio
    async def test_core_batch_all_errors_collects_all(self):
        result = [{"error": 1}, {"error": 7}]
        with pytest.raises(WialonInvalidResult) as exc_info:
            await WialonCallRespValidator.validate_result("core_batch", result)
        assert len(exc_info.value.reason) == 2


# ---------------------------------------------------------------------------
# validate_headers
# ---------------------------------------------------------------------------

class TestValidateHeaders:
    def _make_response(self, content_type):
        response = MagicMock()
        response.headers = {"Content-Type": content_type} if content_type else {}
        return response

    @pytest.mark.asyncio
    async def test_json_content_type_no_warning(self, recwarn):
        response = self._make_response("application/json")
        await WialonCallRespValidator.validate_headers(response)
        assert len(recwarn) == 0

    @pytest.mark.asyncio
    async def test_missing_content_type_warns(self, recwarn):
        response = self._make_response(None)
        await WialonCallRespValidator.validate_headers(response)
        assert len(recwarn) == 1

    @pytest.mark.asyncio
    async def test_wrong_content_type_warns(self, recwarn):
        response = self._make_response("text/html")
        await WialonCallRespValidator.validate_headers(response)
        assert len(recwarn) == 1


# ---------------------------------------------------------------------------
# has_attachment
# ---------------------------------------------------------------------------

class TestHasAttachment:
    def _make_response(self, content_type="application/json", content_disposition=None):
        response = MagicMock()
        headers = {"Content-Type": content_type}
        if content_disposition:
            headers["Content-Disposition"] = content_disposition
        response.headers = headers
        return response

    @pytest.mark.asyncio
    async def test_json_no_attachment(self):
        response = self._make_response()
        assert await WialonCallRespValidator.has_attachment(response) is False

    @pytest.mark.asyncio
    async def test_attachment_disposition(self):
        response = self._make_response(
            content_disposition='attachment; filename="file.wlp"'
        )
        assert await WialonCallRespValidator.has_attachment(response) is True

    @pytest.mark.asyncio
    async def test_octet_stream(self):
        response = self._make_response(content_type="application/octet-stream")
        assert await WialonCallRespValidator.has_attachment(response) is True

    @pytest.mark.asyncio
    async def test_multipart(self):
        response = self._make_response(content_type="multipart/form-data")
        assert await WialonCallRespValidator.has_attachment(response) is True
