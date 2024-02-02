from .misc import *

def read_site_config(id):
    return readJSON(f"{SITES_CONFIG_DIR}/{id}.site")

def generate_site_config():
    config = {}
    for key, setting_section in readJSON(f"{SITE_CONFIG_MAP}").items():
        config[key] = {}
        for key_option, option in setting_section.items():
            config[key][key_option] = option["default"]
    return config
