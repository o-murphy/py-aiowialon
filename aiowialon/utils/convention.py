from typing import Any, Dict


def prepare_action_name(action_name: str) -> str:
    return action_name.replace('_', '/', 1)


def prepare_action_params(params: dict) -> dict:
    if not isinstance(params, dict):
        return params

    new_params: Dict[str, Any] = {}
    for k, v in params.items():
        # Remove trailing underscores
        new_key = k.rstrip('_') if k.endswith('_') else k

        # Convert CapitalisedKey to capitalisedParam
        new_key = new_key[:1].lower() + new_key[1:] if new_key else ''

        # Process nested dictionaries and lists
        if isinstance(v, dict):
            new_params[new_key] = prepare_action_params(v)
        elif isinstance(v, list):
            new_params[new_key] = [prepare_action_params(item) if isinstance(item, dict) else item for
                                   item in v]
        else:
            new_params[new_key] = v
    return new_params
