import json
import os

VERSION = "0.2.0"

# Paths
CONFIG_DIR = "config"
CONFIG_FILE = "config.json"
POINTS_CONFIG_DIR = CONFIG_DIR + "/points"
POINT_CONFIG_MAP = CONFIG_DIR + "/point_config_map.json"
POINTS_DIR = "points"
ADDONS_FILE = "addons.json"
SERVER_FILE = "server.py"



def setup_MorePoints():
    if not os.path.exists(POINTS_DIR):
        os.makedirs(POINTS_DIR)

def list_points():
    points = []
    for file in os.listdir(POINTS_CONFIG_DIR):
        if file.endswith(".point"):
            data = readJSON(f"{POINTS_CONFIG_DIR}/{file}")
            points.append({
                "name": file[0:-6],
                "data": data.get("Point", {})
            })
    return points

def updateAddons():
    return readJSON(f"{CONFIG_DIR}/{ADDONS_FILE}")

def readJSON(src):
    with open(src,"r") as file:
        try:
            return json.load(file)
        except:
            return {}

def writeJSON(src, data):
    with open(src,"w") as file:
        json.dump(data, file, indent=4)

def human_readable_size(num, suffix="B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"
