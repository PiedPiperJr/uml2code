import json

def dump(file_path, data):
    # dump. . .
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
