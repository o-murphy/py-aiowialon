from typing import Optional


class WialonError(Exception):
    """
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
        1001: 'No message for selected interval',
        1002: 'Item with such unique property already exists',
        1003: 'Only one request of given time is allowed at the moment'
    }

    def __init__(self, code: int, reason: Optional[str] = None, action_name: Optional[str] = None):
        self.code = code
        self.reason = reason
        self.action_name = action_name
        try:
            self.code = int(code)
        except ValueError:
            pass

    def __str__(self):
        explanation = WialonError.errors.get(self.code, 6)
        action_name = f'"{self.action_name}" ' if self.action_name else ""
        reason = f": {self.reason}" if self.reason else ""
        message = '{error} {action_name}({code}){reason}'.format(
            error=explanation,
            code=self.code,
            reason=reason,
            action_name=action_name)
        return 'WialonError({message})'.format(message=message)

    def __repr__(self):
        return str(self)


class WialonInvalidSession(WialonError, PermissionError):

    def __init__(self, reason: Optional[str] = None, action_name: Optional[str] = None):
        super().__init__(1, reason, action_name)


class WialonInvalidService(WialonError, LookupError):

    def __init__(self, reason: Optional[str] = None, action_name: Optional[str] = None):
        super().__init__(2, reason, action_name)


class WialonInvalidResult(WialonError, RuntimeError):

    def __init__(self, reason: Optional[str] = None, action_name: Optional[str] = None):
        super().__init__(3, reason, action_name)


class WialonInvalidInput(WialonError, ValueError):

    def __init__(self, reason: Optional[str] = None, action_name: Optional[str] = None):
        super().__init__(4, reason, action_name)


class WialonErrorPerformingRequest(WialonError, RuntimeError):

    def __init__(self, reason: Optional[str] = None, action_name: Optional[str] = None):
        super().__init__(5, reason, action_name)


class WialonUnknownError(WialonError, Exception):

    def __init__(self, reason: Optional[str] = None, action_name: Optional[str] = None):
        super().__init__(6, reason, action_name)


class WialonAccessDenied(WialonError, PermissionError):

    def __init__(self, reason: Optional[str] = None, action_name: Optional[str] = None):
        super().__init__(7, reason, action_name)


class WialonInvalidCredentials(WialonError, PermissionError):

    def __init__(self, reason: Optional[str] = None, action_name: Optional[str] = None):
        super().__init__(8, reason, action_name)


class WialonAuthServerUnavailableError(WialonError, ConnectionError):

    def __init__(self, reason: Optional[str] = None, action_name: Optional[str] = None):
        super().__init__(9, reason, action_name)


class WialonMessageNotFoundError(WialonError, ValueError):

    def __init__(self, reason: Optional[str] = None, action_name: Optional[str] = None):
        super().__init__(1001, reason, action_name)


class WialonDuplicateItemError(WialonError, LookupError):

    def __init__(self, reason: Optional[str] = None, action_name: Optional[str] = None):
        super().__init__(1002, reason, action_name)


class WialonRequestLimitExceededError(WialonError, RuntimeError):

    def __init__(self, reason: Optional[str] = None, action_name: Optional[str] = None):
        super().__init__(1003, reason, action_name)


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
    1001: WialonMessageNotFoundError,
    1002: WialonDuplicateItemError,
    1003: WialonRequestLimitExceededError
}
