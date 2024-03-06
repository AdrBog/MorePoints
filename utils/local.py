"""
This module contains methods to perform file actions locally.
"""
from flask import jsonify
from io import BytesIO, StringIO
import os
import re
import time
import shutil
from .config import *
from .msg import *



def local_create_folder(id, path, filename):
	local_data = read_point_config(id).get("Local", {})
	dir = local_data.get("Path", "/")
	try:
		output = os.mkdir(f"{dir}/{path}/{filename}")
		return jsonify(status="Ok", output=output)
	except Exception as error:
		return jsonify(status="Error", output=str(error))

def local_create_file(id, path, filename, content):
	local_data = read_point_config(id).get("Local", {})
	dir = local_data.get("Path", "/")
	try:
		with open(f"{dir}/{path}/{filename}", "wb") as f:
			output = f.write(content.encode())
			return jsonify(status="Ok", output=output)
	except Exception as error:
		return jsonify(status="Error", output=str(error))

def local_upload_file(id, path, files):
	local_data = read_point_config(id).get("Local", {})
	dir = local_data.get("Path", "/")
	try:
		for file in files:
			with open(f"{dir}/{path}/{file.filename}", "wb") as f:
				output = f.write(file.read())
		return jsonify(status="Ok", output=output)
	except Exception as error:
		return jsonify(status="Error", output=str(error))

def local_delete_file(id, path, filename):
	local_data = read_point_config(id).get("Local", {})
	dir = local_data.get("Path", "/")
	try:
		if os.path.isdir(f"{dir}/{path}/{filename}"):
			output = shutil.rmtree(f"{dir}/{path}/{filename}")
		else:
			output = os.remove(f"{dir}/{path}/{filename}")
		return jsonify(status="Ok", output=output)
	except Exception as error:
		return jsonify(status="Error", output=str(error))

def local_rename_file(id, path, newpath, filename, newname):
	local_data = read_point_config(id).get("Local", {})
	dir = local_data.get("Path", "/")
	try:
		output = os.rename(f"{dir}/{path}/{filename}", f"{dir}/{newpath}/{newname}")
		return jsonify(status="Ok", output=output)
	except Exception as error:
		return jsonify(status="Error", output=str(error))

def local_read_file(id, path):
	local_data = read_point_config(id).get("Local", {})
	file = local_data.get("Path", "/") + path
	with open(file, "rb") as f:
		return f.read()

def local_list_dir(id, path = "/"):
	local_data = read_point_config(id).get("Local", {})
	dir = local_data.get("Path", "/")
	files = []
	for f in os.listdir(f"{dir}/{path}"):
		file_stats = os.stat(f"{dir}/{path}/{f}")
		files.append([f, {
			"size": file_stats.st_size,
			"modify": time.ctime(os.path.getmtime(f"{dir}/{path}/{f}")),
			"type": "dir" if os.path.isdir(f"{dir}/{path}/{f}") else "file"
		}])
	return files

def local_list_dir_filter(id, dir = "/", search = ""):
	files = local_list_dir(id, dir)
	regex = re.compile(search)
	filter_search = [f for f in files if regex.match(f[0])]
	return filter_search
