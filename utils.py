import json


def read_json_file(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


def read_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
        return content
