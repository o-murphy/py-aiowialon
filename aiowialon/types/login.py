from typing import TypedDict, Optional, Callable, Coroutine


class LoginParams(TypedDict, total=False):
    token: Optional[str]
    hash: Optional[str]
    appName: Optional[str]
    operateAs: Optional[str]
    fl: Optional[str]
    checkService: Optional[str]


OnLoginCallback = Callable[[], Coroutine]


__all__ = ('LoginParams', 'OnLoginCallback')
