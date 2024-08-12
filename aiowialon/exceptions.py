"""Definitions of Wialon Remote API exceptions."""
from typing import Optional, Any, Union, List

# pylint: skip-file

WialonErrorReason = Union[str, int, 'WialonError', List['WialonError']]


class WialonError(Exception):
    """
    Base Wialon exception class.
    Exception raised when a Wialon Remote API call fails due to a network
    related error or for a Wialon specific reason.
    """
    errors = {
        1: 'Invalid session',
        2: 'Invalid service',
        3: 'Invalid result',
        4: 'Invalid input',
        5: 'Error performing request',
        6: 'Unknown error',
        7: 'Access denied',
        8: 'Invalid user name or password',
        9: 'Authorization server is unavailable, please try again later',
        10: 'Reached limit of concurrent requests',
        11: 'Password reset error',
        14: 'Billing error',
        1001: 'No message for selected interval',
        1002: 'Item with such unique property already exists '
              'or Item cannot be created according to billing restrictions',
        1003: 'Only one request of given time is allowed at the moment',
        1004: 'Limit of messages has been exceeded',
        1005: 'Execution time has exceeded the limit',
        1006: 'Exceeding the limit of attempts to enter a two-factor authorization code',
        1011: 'Your IP has changed or session has expired',
        2006: 'No possible to transfer unit to this account',
        2008: 'User does not have access to unit (due transferring to new account)',
        2014: 'Selected user is a creator for some system objects, '
              'thus this user cannot be bound to a new account',
        2015: 'Sensor deleting is forbidden because of using '
              'in another sensor or advanced properties of the unit',
    }

    def __init__(self, code: int,
                 reason: Optional[WialonErrorReason] = None,
                 action_name: Optional[str] = None,
                 result: Optional[Any] = None):

        self.code: int = code
        self.reason: Optional[WialonErrorReason] = reason
        self.action_name: Optional[str] = action_name
        self.result: Optional[Any] = result
        try:
            self.code = int(code)
        except ValueError:
            pass

    def __str__(self):
        explanation = WialonError.errors.get(self.code, 6)
        action_name = f'"{self.action_name}" ' if self.action_name else ""
        reason = ""
        if self.reason is not None:
            if isinstance(self.reason, (WialonError, str)):
                reason = f": {self.reason}"
            elif isinstance(self.reason, (list, tuple)):
                if any(isinstance(element, WialonError) for element in self.reason):
                    reason = ": use 'WialonError.reason' method, to get details"
        return f'{explanation} {action_name}({self.code}){reason}'

    def __repr__(self):
        return str(self)


class WialonInvalidSession(WialonError, PermissionError):

    def __init__(self, reason: Optional[WialonErrorReason] = None,
                 action_name: Optional[str] = None,
                 result: Optional[Any] = None):
        super().__init__(1, reason, action_name, result)


class WialonInvalidService(WialonError, LookupError):

    def __init__(self, reason: Optional[WialonErrorReason] = None,
                 action_name: Optional[str] = None,
                 result: Optional[Any] = None):
        super().__init__(2, reason, action_name, result)


class WialonInvalidResult(WialonError, RuntimeError):

    def __init__(self, reason: Optional[WialonErrorReason] = None,
                 action_name: Optional[str] = None,
                 result: Optional[Any] = None):
        super().__init__(3, reason, action_name, result)


class WialonInvalidInput(WialonError, ValueError):

    def __init__(self, reason: Optional[WialonErrorReason] = None,
                 action_name: Optional[str] = None,
                 result: Optional[Any] = None):
        super().__init__(4, reason, action_name, result)


class WialonErrorPerformingRequest(WialonError, RuntimeError):

    def __init__(self, reason: Optional[WialonErrorReason] = None,
                 action_name: Optional[str] = None,
                 result: Optional[Any] = None):
        super().__init__(5, reason, action_name, result)


class WialonUnknownError(WialonError, Exception):

    def __init__(self, reason: Optional[WialonErrorReason] = None,
                 action_name: Optional[str] = None,
                 result: Optional[Any] = None):
        super().__init__(6, reason, action_name, result)


class WialonAccessDenied(WialonError, PermissionError):

    def __init__(self, reason: Optional[WialonErrorReason] = None,
                 action_name: Optional[str] = None,
                 result: Optional[Any] = None):
        super().__init__(7, reason, action_name, result)


class WialonInvalidCredentials(WialonError, PermissionError):

    def __init__(self, reason: Optional[WialonErrorReason] = None,
                 action_name: Optional[str] = None,
                 result: Optional[Any] = None):
        super().__init__(8, reason, action_name, result)


class WialonAuthServerUnavailableError(WialonError, ConnectionError):

    def __init__(self, reason: Optional[WialonErrorReason] = None,
                 action_name: Optional[str] = None,
                 result: Optional[Any] = None):
        super().__init__(9, reason, action_name, result)


class WialonReachedConcurrentRequestLimit(WialonError, RuntimeError):
    def __init__(self, reason: Optional[WialonErrorReason] = None,
                 action_name: Optional[str] = None,
                 result: Optional[Any] = None):
        super().__init__(10, reason, action_name, result)


class WialonPasswordResetError(WialonError, RuntimeError):
    def __init__(self, reason: Optional[WialonErrorReason] = None,
                 action_name: Optional[str] = None,
                 result: Optional[Any] = None):
        super().__init__(11, reason, action_name, result)


class WialonBillingError(WialonError, RuntimeError):
    def __init__(self, reason: Optional[WialonErrorReason] = None,
                 action_name: Optional[str] = None,
                 result: Optional[Any] = None):
        super().__init__(14, reason, action_name, result)


class WialonMessageNotFoundError(WialonError, ValueError):

    def __init__(self, reason: Optional[WialonErrorReason] = None,
                 action_name: Optional[str] = None,
                 result: Optional[Any] = None):
        super().__init__(1001, reason, action_name, result)


class WialonDuplicateItemError(WialonError, LookupError):

    def __init__(self, reason: Optional[WialonErrorReason] = None,
                 action_name: Optional[str] = None,
                 result: Optional[Any] = None):
        super().__init__(1002, reason, action_name, result)


class WialonRequestLimitExceededError(WialonError, RuntimeError):
    _reasons = {
        1: 'Only one request is allowed at the moment',
        2: 'LIMIT api_concurrent',
        3: 'LAYERS_MAX_COUNT',
        4: 'NO_SESSION',
        5: 'LOCKER_ERROR',
    }

    def __init__(self, reason: Optional[WialonErrorReason] = None,
                 action_name: Optional[str] = None,
                 result: Optional[Any] = None):
        if isinstance(reason, int):
            reason = self._reasons.get(reason, reason)
        super().__init__(1003, reason, action_name, result)


class WialonMessageLimitExceededError(WialonError, RuntimeError):
    def __init__(self, reason: Optional[WialonErrorReason] = None,
                 action_name: Optional[str] = None,
                 result: Optional[Any] = None):
        super().__init__(1004, reason, action_name, result)


class WialonExecutionTimeExceededError(WialonError, RuntimeError):
    def __init__(self, reason: Optional[WialonErrorReason] = None,
                 action_name: Optional[str] = None,
                 result: Optional[Any] = None):
        super().__init__(1005, reason, action_name, result)


class WialonTwoFactorAuthAttemptsExceededError(WialonError, PermissionError):
    def __init__(self, reason: Optional[WialonErrorReason] = None,
                 action_name: Optional[str] = None,
                 result: Optional[Any] = None):
        super().__init__(1006, reason, action_name, result)


class WialonSessionExpiredOrIPChangedError(WialonError, RuntimeError):
    def __init__(self, reason: Optional[WialonErrorReason] = None,
                 action_name: Optional[str] = None,
                 result: Optional[Any] = None):
        super().__init__(1011, reason, action_name, result)


class WialonTransferUnitError(WialonError, RuntimeError):
    def __init__(self, reason: Optional[WialonErrorReason] = None,
                 action_name: Optional[str] = None,
                 result: Optional[Any] = None):
        super().__init__(2006, reason, action_name, result)


class WialonAccessDeniedDueToTransferError(WialonError, PermissionError):
    def __init__(self, reason: Optional[WialonErrorReason] = None,
                 action_name: Optional[str] = None,
                 result: Optional[Any] = None):
        super().__init__(2008, reason, action_name, result)


class WialonUserCreationError(WialonError, RuntimeError):
    def __init__(self, reason: Optional[WialonErrorReason] = None,
                 action_name: Optional[str] = None,
                 result: Optional[Any] = None):
        super().__init__(2014, reason, action_name, result)


class WialonSensorDeleteForbiddenError(WialonError, RuntimeError):
    def __init__(self, reason: Optional[WialonErrorReason] = None,
                 action_name: Optional[str] = None,
                 result: Optional[Any] = None):
        super().__init__(2015, reason, action_name, result)


WIALON_EXCEPTIONS = {
    1: WialonInvalidSession,
    2: WialonInvalidService,
    3: WialonInvalidResult,
    4: WialonInvalidInput,
    5: WialonErrorPerformingRequest,
    6: WialonUnknownError,
    7: WialonAccessDenied,
    8: WialonInvalidCredentials,
    9: WialonAuthServerUnavailableError,
    10: WialonReachedConcurrentRequestLimit,
    11: WialonPasswordResetError,
    14: WialonBillingError,
    1001: WialonMessageNotFoundError,
    1002: WialonDuplicateItemError,
    1003: WialonRequestLimitExceededError,
    1004: WialonMessageLimitExceededError,
    1005: WialonExecutionTimeExceededError,
    1006: WialonTwoFactorAuthAttemptsExceededError,
    1011: WialonSessionExpiredOrIPChangedError,
    2006: WialonTransferUnitError,
    2008: WialonAccessDeniedDueToTransferError,
    2014: WialonUserCreationError,
    2015: WialonSensorDeleteForbiddenError,
}


class WialonWarning(UserWarning):
    """Wialon UserWarning"""


__all__ = ['WialonError', 'WialonWarning']
__all__ += [n.__name__ for n in WIALON_EXCEPTIONS.values()]
