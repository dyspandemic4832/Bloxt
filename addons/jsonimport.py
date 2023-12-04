import json

class JsonImport:
    def __init__(self, json_file) -> None:
        self.config_filename = json_file
        self.config_file = cache_config_file(self.config_filename)

    def get_value_from_key(self, key):
        return self.config_file[key]

def cache_config_file(config_name):
    with open(config_name, "r") as read_file:
        config_file = json.load(read_file)
        return config_file