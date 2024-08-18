import warnings
from abc import ABC

from typing_extensions import Any, Coroutine, Unpack

from aiowialon import Wialon
from aiowialon.exceptions import WialonWarning
from aiowialon.types.api_types import core


class WialonService(ABC):
    def __init__(self, name: str, client: Wialon):
        self.name = name
        self.client = client

    def __getattr__(self, action_name: str) -> Any:
        """
        Enable the calling of Wialon API methods through Python method calls
        of the same name.
        """

        def get(_self, *args, **kwargs):
            return self.client.call(f"{self.name}_{action_name}", *args, **kwargs)

        return get.__get__(self, object)


class WialonCore(WialonService):
    def __init__(self, client: Wialon):
        super().__init__("core", client)

    def _logout(self) -> Coroutine[Any, Any, core.CoreErrorCode]:
        """Warn on direct usage"""
        warnings.warn("Don't recommend using "
                      "'Wialon.core.logout' method directly, "
                      "use 'Wialon.logout' or 'Wialon.stop_polling' instead",
                      WialonWarning)

        # Await the call directly, no need to wrap in another function
        return self.client.call("core_logout")

    def _batch(self, **params: Unpack[core.CoreBatchParams]) -> Coroutine[Any, Any, core.CoreBatchResponse]:
        """Warn on direct usage"""
        warnings.warn("Don't recommend using "
                      "'Wialon.core.batch' method directly, "
                      "use 'Wialon.batch' instead",
                      WialonWarning)
        return self.client.call("core_batch", **params)
