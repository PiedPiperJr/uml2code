from typing import Any, Union
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

