"""Tests for aiowialon.exceptions"""

import pytest

from aiowialon.exceptions import (
    WIALON_EXCEPTIONS,
    WialonError,
    WialonInvalidSession,
    WialonAccessDenied,
    WialonRequestLimitExceededError,
    WialonUnknownError,
    WialonWarning,
)


class TestWialonError:
    def test_known_code_str(self):
        err = WialonError(1)
        assert "Invalid session" in str(err)
        assert "(1)" in str(err)

    def test_unknown_code_str_shows_unknown_error_text(self):
        err = WialonError(9999)
        assert "Unknown error" in str(err)
        assert "(9999)" in str(err)

    def test_str_with_action_name(self):
        err = WialonError(7, action_name="core_search_item")
        assert '"core_search_item"' in str(err)

    def test_str_with_string_reason(self):
        err = WialonError(4, reason="bad param")
        assert "bad param" in str(err)

    def test_str_with_wialon_error_reason(self):
        inner = WialonError(3)
        err = WialonError(3, reason=inner)
        assert str(inner) in str(err)

    def test_str_with_list_reason(self):
        inner = WialonError(3)
        err = WialonError(3, reason=[inner])
        assert "reason" in str(err).lower() or "details" in str(err).lower()

    def test_code_stored_as_int(self):
        err = WialonError(7)
        assert err.code == 7
        assert isinstance(err.code, int)

    def test_repr_equals_str(self):
        err = WialonError(1)
        assert repr(err) == str(err)

    def test_result_attribute(self):
        result = {"error": 5}
        err = WialonError(5, result=result)
        assert err.result is result


class TestWialonSubclasses:
    def test_invalid_session_is_permission_error(self):
        err = WialonInvalidSession()
        assert isinstance(err, PermissionError)
        assert err.code == 1

    def test_access_denied_is_permission_error(self):
        err = WialonAccessDenied()
        assert isinstance(err, PermissionError)
        assert err.code == 7

    def test_request_limit_exceeded_reason_mapping(self):
        err = WialonRequestLimitExceededError(reason=1)
        assert "one request" in str(err).lower() or err.reason == "Only one request is allowed at the moment"

    def test_request_limit_exceeded_unknown_reason_passthrough(self):
        err = WialonRequestLimitExceededError(reason=99)
        assert err.reason == 99

    def test_unknown_error_code(self):
        err = WialonUnknownError()
        assert err.code == 6


class TestWialonExceptionsMapping:
    def test_all_known_codes_have_exception_class(self):
        for code in WialonError.errors:
            if code in WIALON_EXCEPTIONS:
                inst = WIALON_EXCEPTIONS[code]()
                assert isinstance(inst, WialonError)

    def test_mapping_keys_match_error_codes(self):
        for code, cls in WIALON_EXCEPTIONS.items():
            inst = cls()
            assert inst.code == code

    def test_wialon_warning_is_user_warning(self):
        assert issubclass(WialonWarning, UserWarning)
