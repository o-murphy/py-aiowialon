"""Declaration of types annotation for the 'login/logout' methods,
and session event callbacks handlers of aio wialon.Wialon client"""

from collections.abc import Awaitable, Callable
from typing import TypedDict

from aiowialon.types.api_types import core, token as token_params


class ClientLoginParams(TypedDict, total=False):
    """
    Types annotation for 'login' and 'start_polling' keyword arguments
    """

    token: str | None
    auth_hash: str | None
    appName: str | None
    operateAs: str | None
    fl: str | None
    checkService: str | None


ClientLoginCallback = Callable[[token_params.TokenLoginResponse], Awaitable[None]]
ClientLogoutCallback = Callable[[core.CoreErrorCode], Awaitable[None]]

__all__ = ("ClientLoginParams", "ClientLoginCallback", "ClientLogoutCallback")
