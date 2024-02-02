import json
import os

VERSION = "0.1.1"

# Paths
CONFIG_DIR = "config"
CONFIG_FILE = "config.json"
SITES_CONFIG_DIR = CONFIG_DIR + "/sites"
SITE_CONFIG_MAP = CONFIG_DIR + "/site_config_map.json"
SITES_DIR = "sites"
ADDONS_FILE = "addons.json"
SERVER_FILE = "server.py"
CACHE_DIR = os.path.expanduser('~') + "/.cache/MorePoints"

# Messages
MSG_ERROR_LOGIN = "You have to login"
MSG_ERROR_FILE_EXISTS = "File already exists"
MSG_ERROR_SITE_NOT_FOUND = "Site not found"
MSG_ERROR_WRONG_PASSWORD = "Wrong password"
MSG_INFO_FILE_SAVED = "File saved"

def updateAddons():
    return readJSON(f"{CONFIG_DIR}/{ADDONS_FILE}")

def readJSON(src):
    with open(src,"r") as file:
        return json.load(file)

def writeJSON(src, data):
    with open(src,"w") as file:
        json.dump(data, file, indent=4)

def human_readable_size(num, suffix="B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"
