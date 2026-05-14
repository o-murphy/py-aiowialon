"""Declaration of types annotation for the 'login/logout' methods,
and session event callbacks handlers of aio wialon.Wialon client"""

from typing import Awaitable, Callable, Optional

from typing_extensions import TypedDict

from aiowialon.types.api_types import core, token as token_params


class ClientLoginParams(TypedDict, total=False):
    """
    Types annotation for 'login' and 'start_polling' keyword arguments
    """

    token: Optional[str]
    auth_hash: Optional[str]
    appName: Optional[str]
    operateAs: Optional[str]
    fl: Optional[str]
    checkService: Optional[str]


ClientLoginCallback = Callable[[token_params.TokenLoginResponse], Awaitable[None]]
ClientLogoutCallback = Callable[[core.CoreErrorCode], Awaitable[None]]

__all__ = ("ClientLoginParams", "ClientLoginCallback", "ClientLogoutCallback")
