"""
Special convention module
to resolve Wialon Remote API specific usage cases with python
"""

from typing import Any, Dict


def prepare_action_name(action_name: str) -> str:
    """
    Uses for replacing a call 'action_name' with Wialon Remote API 'svc' name
    Example:
    >>> 'core_search_item' -> 'core/search_item'
    >>> 'unit_group_update_groups' -> 'unit_group/search_item'
    """
    act_name = action_name.lower()
    if act_name.startswith('unit_group'):
        return "unit_group" + "/" + act_name[len('unit_group')+1:]
    return act_name.replace('_', '/', 1)


def prepare_action_params(params: dict) -> dict:
    """
    Resolves params names conflicts with Wialon Remote API.
    Replaces parameters names with adjusted to Wialon Remote API
    It allows to use python's reserved words as request params names
    with adding leading and traileng underscores to its names
    and use Capitalised names for API Calls.
    Removes trailing and leading underscores and replaces firs letter with lowercase
    Example:
    >>> 'from_' -> 'from'
    >>> 'ItemId' -> 'itemId'
    >>> '_id' -> 'id'
    """

    if not isinstance(params, dict):
        return params

    new_params: Dict[str, Any] = {}
    for k, v in params.items():
        # Remove trailing underscores
        new_key = k.strip('_')

        # Convert CapitalisedKey to capitalisedParam
        new_key = new_key[:1].lower() + new_key[1:] if new_key else ''

        # Process nested dictionaries and lists
        if isinstance(v, dict):
            new_params[new_key] = prepare_action_params(v)
        elif isinstance(v, list):
            new_params[new_key] = [prepare_action_params(item)
                                   if isinstance(item, dict)
                                   else item for item in v]
        else:
            new_params[new_key] = v
    return new_params


__all__ = (
    'prepare_action_name',
    'prepare_action_params'
)
