"""Declaration of types annotation for the 'login/logout' methods,
and session event callbacks handlers of aio wialon.Wialon client"""

from typing_extensions import TypedDict, Optional, Callable, Coroutine
from aiowialon.types.api_types import core, token as token_params


class ClientLoginParams(TypedDict, total=False):
    """
    Types annotation for 'login' and 'start_polling' keyword arguments
    """

    token: Optional[str]
    hash: Optional[str]
    appName: Optional[str]
    operateAs: Optional[str]
    fl: Optional[str]
    checkService: Optional[str]


ClientLoginCallback = Callable[[token_params.TokenLoginResponse], Coroutine]
ClientLogoutCallback = Callable[[core.CoreErrorCode], Coroutine]

__all__ = ('ClientLoginParams', 'ClientLoginCallback', 'ClientLogoutCallback')
