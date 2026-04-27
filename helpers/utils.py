from typing import Any, Union


def lowercase_keys(data: Union[dict, list, Any]) -> Union[dict, list, Any]:
    if isinstance(data, dict):
        return {
            k.lower() if isinstance(k, str) else k: lowercase_keys(v)
            for k, v in data.items()
        }
    if isinstance(data, list):
        return [lowercase_keys(item) for item in data]
    return data


def capitalize(s: str) -> str:
    return s[0].upper() + s[1:] if s else s


def lower_first(s: str) -> str:
    return s[0].lower() + s[1:] if s else s


def snake_to_pascal(s: str) -> str:
    return ''.join(capitalize(word) for word in s.split('_'))
