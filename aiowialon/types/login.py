"""Declaration of types annotation for the 'login/logout' methods,
and session event callbacks handlers of aio wialon.Wialon client"""

from typing import TypedDict, Optional, Callable, Coroutine, Any


class LoginParams(TypedDict, total=False):
    """
    Types annotation for 'login' and 'start_polling' keyword arguments
    """

    token: Optional[str]
    hash: Optional[str]
    appName: Optional[str]
    operateAs: Optional[str]
    fl: Optional[str]
    checkService: Optional[str]


LoginCallback = Callable[[Any], Coroutine]
LogoutCallback = Callable[[Any], Coroutine]


__all__ = ('LoginParams', 'LoginCallback', 'LogoutCallback')
