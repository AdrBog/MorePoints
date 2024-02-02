from .misc import *

def read_point_config(id):
    return readJSON(f"{POINTS_CONFIG_DIR}/{id}.point")

def generate_point_config():
    config = {}
    for key, setting_section in readJSON(f"{POINT_CONFIG_MAP}").items():
        config[key] = {}
        for key_option, option in setting_section.items():
            config[key][key_option] = option["default"]
    return config
