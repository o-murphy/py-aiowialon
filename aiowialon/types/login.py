from typing import TypedDict, Optional, Callable, Coroutine, Any, Dict


class LoginParams(TypedDict, total=False):
    token: Optional[str]
    hash: Optional[str]
    appName: Optional[str]
    operateAs: Optional[str]
    fl: Optional[str]
    checkService: Optional[str]


OnLoginCallback = Callable[[Dict[str, Any]], Coroutine]
OnLogoutCallback = Callable[[Dict[str, Any]], Coroutine]


__all__ = ('LoginParams', 'OnLoginCallback', 'OnLogoutCallback')
