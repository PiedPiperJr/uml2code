import json

def dump(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def snake_to_pascal(snake_str):
    return capitalize(''.join(capitalize(word) for word in snake_str.split('_')))

def capitalize(input_str:str):
    return input_str[0].upper() + input_str[1:]