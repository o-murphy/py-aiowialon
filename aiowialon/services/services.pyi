from _typeshed import Incomplete
from abc import ABC
from aiowialon import Wialon as Wialon
from typing_extensions import Any, Unpack

from aiowialon.types.api_types import core


class WialonService(ABC):
    name: Incomplete
    client: Incomplete
    def __init__(self, name: str, client: Wialon) -> None: ...
    def __getattr__(self, action_name: str) -> Any: ...

class WialonCore(WialonService):
    def __init__(self, client: Wialon) -> None: ...

    """
    References to core service
    https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/core/core
    """
    def _logout(self) -> core.CoreErrorCode: ...
    def _batch(self, **params: Unpack[core.CoreBatchParams]) -> core.CoreBatchResponse: ...

    async def get_account_data(self, **params: Unpack[core.CoreGetAccountDataParams]) -> core.CoreGetAccountDataResponse: ...
    async def check_items_billing(self, **params: Unpack[core.CoreChechItemsBillingParams]) -> core.CoreChechItemsBillingResponse: ...
    async def check_accessors(self, **params: Unpack[core.CoreCheckAccessorsParams]) -> core.CoreCheckAccessorsResponse: ...
    async def create_user(self, **params: Unpack[core.CoreCreateUserParams]) -> core.CoreCreateUserResponse: ...
    async def create_resource(self, **params: Unpack[core.CoreCreateResourceParams]) -> core.CoreCreateResourceResponse: ...
    async def create_unit(self, **params: Unpack[core.CoreCreateUnitParams]) -> core.CoreCreateUnitResponse: ...
    async def create_unit_group(self, **params: Unpack[core.CoreCreateUnitGroupParams]) -> core.CoreCreateUnitGroupResponse: ...
    async def create_retranslator(self, **params: Unpack[core.CoreCreateRetranslatorParams]) -> core.CoreCreateRetranslatorResponse: ...
    async def create_route(self, **params: Unpack[core.CoreCreateRouteParams]) -> core.CoreCreateRouteResponse: ...
    async def search_item(self, **params: Unpack[core.CoreSearchItemParams]) -> core.CoreSearchItemResponse: ...
    async def search_items(self, **params: Unpack[core.CoreSearchItemsParams]) -> core.CoreSearchItemsResponse: ...
    async def update_data_flags(self, **params: Unpack[core.CoreUpdateDataFlagsParams]) -> core.CoreUpdateDataFlagsResponse: ...
    async def get_hw_types(self, **params: Unpack[core.CoreGetHwTypesParams]) -> core.CoreGetHwTypesResponse: ...
    async def get_hw_cmds(self, **params: Unpack[core.CoreGetHwCommandsParams]) -> core.CoreGetHwCommandsTemplates: ...
    async def reset_password_request(self, **params: Unpack[core.CoreResetPasswordRequestParams]) -> core.CoreErrorCode: ...
    async def reset_password_perform(self, **params: Unpack[core.CoreResetPasswordPerformParams]) -> core.CoreResetPasswordPerformResponse: ...
    async def duplicate(self, **params: Unpack[core.CoreDuplicateParams]) -> core.CoreDuplicateResponse: ...
    async def create_auth_hash(self) -> core.CoreCreateAuthHashResponse: ...
    async def use_auth_hash(self, **params: Unpack[core.CoreUseAuthHashParams]) -> core.CoreUseAuthHashResponse: ...
    async def check_unique(self, **params: Unpack[core.CoreCheckUniqueParams]) -> core.CoreCheckUniqueResponse: ...
    async def export_file(self, **params: Unpack[core.CoreSearchItemsParams]) -> bytes: ...
    async def set_session_property(self, **params: Unpack[core.CoreSessionPropertyParams]) -> core.CoreSessionPropertyResponse: ...