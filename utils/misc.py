"""
This module contains general methods and variables that I did not know how to categorize.
"""
import json
import os
from flask import render_template

VERSION = "0.3.0"

# Paths
CONFIG_DIR = "config"
CONFIG_FILE = "config.json"
POINTS_CONFIG_DIR = CONFIG_DIR + "/points"
POINT_CONFIG_MAP = CONFIG_DIR + "/point_config_map.json"
ADDONS_FILE = "addons.json"

def display_error_page(error):
    return render_template("error.html", error=error, errname=type(error).__name__)

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
    if num is None:
        num = 0
    elif type(num) is str:
        num = int(num)
    
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"
