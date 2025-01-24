import json

def dump(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def snake_to_pascal(snake_str):
    return ''.join(word.capitalize() for word in snake_str.split('_'))