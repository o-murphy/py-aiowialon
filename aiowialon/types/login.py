from typing import TypedDict, Optional, Callable, Coroutine, Any


class LoginParams(TypedDict, total=False):
    token: Optional[str]
    hash: Optional[str]
    appName: Optional[str]
    operateAs: Optional[str]
    fl: Optional[str]
    checkService: Optional[str]


LoginCallback = Callable[[Any], Coroutine]
LogoutCallback = Callable[[Any], Coroutine]


__all__ = ('LoginParams', 'LoginCallback', 'LogoutCallback')
