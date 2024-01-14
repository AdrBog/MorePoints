from io import BytesIO, StringIO
import json
import ftplib

# Paths
CONFIG_DIR = "config"
SITES_CONFIG_DIR = CONFIG_DIR + "/sites"
SITE_CONFIG_MAP = CONFIG_DIR + "/site_config_map.json"
SITES_DIR = "sites"
CONFIG_FILE = "config.json"
ADDONS_FILE = "addons.json"
SERVER_FILE = "server.py"

# Messages
MSG_ERROR_LOGIN = "You have to login"
MSG_ERROR_FILE_EXISTS = "File already exists"
MSG_ERROR_SITE_NOT_FOUND = "Site not found"
MSG_ERROR_WRONG_PASSWORD = "Wrong password"
MSG_INFO_FILE_SAVED = "File saved"

def connect(id):
    ftp = ftplib.FTP('127.0.0.1')
    ftp_data = read_site_config(id)
    ftp.login(id, ftp_data["FTP"]["Password"])
    return ftp

def updateAddons():
    return readJSON(f"{CONFIG_DIR}/{ADDONS_FILE}")

def read_file(id, path):
    ftp = connect(id)
    r = BytesIO()
    ftp.retrbinary(f'RETR /{path}', r.write)
    ftp.quit()
    return r.getvalue()

def remove_dir(ftp, path):
    for (name, properties) in ftp.mlsd(path=path):
        if name in ['.', '..']:
            continue
        elif properties['type'] == 'file':
            ftp.delete(f"{path}/{name}")
        elif properties['type'] == 'dir':
            remove_dir(ftp, f"{path}/{name}")
    ftp.rmd(path)

def read_site_config(id):
    return readJSON(f"{SITES_CONFIG_DIR}/{id}.site")

def readJSON(src):
    with open(src,"r") as file:
        return json.load(file)

def writeJSON(src, data):
    with open(src,"w") as file:
        json.dump(data, file, indent=4)

def generate_site_config():
    config = {}
    for key, setting_section in readJSON(f"{SITE_CONFIG_MAP}").items():
        config[key] = {}
        for key_option, option in setting_section.items():
            config[key][key_option] = option["default"]
    return config

def human_readable_size(num, suffix="B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"