from typing import Any, Dict, Union
import json

class Utils:
    @staticmethod
    def lowercase_keys(data: Union[dict[Any, Any], list[Any]]) -> Union[dict[Any, Any], list[Any], Any]:
        if isinstance(data, dict):
            return {
                k.lower() if isinstance(k, str) else k: Utils.lowercase_keys(v)
                for k, v in data.items()
            }
        elif isinstance(data, list):
            return [Utils.lowercase_keys(item) for item in data]
        else:
            return data
    
    @staticmethod
    def dump(file_path, data):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def snake_to_pascal(snake_str):
        return Utils.capitalize(''.join(Utils.capitalize(word) for word in snake_str.split('_')))

    @staticmethod
    def capitalize(input_str:str):
        if input_str == "":
            return input_str
        return input_str[0].upper() + input_str[1:]

    @staticmethod
    def parse_style_string(style_str: str) -> Dict[str, str]:
        """Helper pour parser la chaîne de style en dictionnaire."""
        if not style_str:
            return {}
        parts = style_str.strip(';').split(';')
        style_dict = {}
        for part in parts:
            if '=' in part:
                key, value = part.split('=', 1)
                style_dict[key.lower()] = value
        return style_dict
