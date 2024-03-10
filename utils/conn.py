"""
This module manages the connection to a point regardless of the protocol used.
"""
from .ftp import *
from .local import *
from flask import redirect

def get_protocol(id):
	point_data = read_point_config(id)
	connection = point_data.get("Connection", {})
	return connection.get("Protocol", "FTP")

def connect(id):
	protocol = get_protocol(id)
	if protocol == "FTP":
		return ftp_connect(id)
	else:
		return None

def create_folder(id, path, filename):
	protocol = get_protocol(id)
	if protocol == "FTP":
		return ftp_create_folder(id, path, filename)
	else:
		return local_create_folder(id, path, filename)

def create_file(id, path, filename, content):
	protocol = get_protocol(id)
	if protocol == "FTP":
		return ftp_create_file(id, path, filename, content)
	else:
		return local_create_file(id, path, filename, content)

def upload_file(id, path, files):
	protocol = get_protocol(id)
	if protocol == "FTP":
		return ftp_upload_file(id, path, files)
	else:
		return local_upload_file(id, path, files)

def delete_file(id, path, filename):
	protocol = get_protocol(id)
	if protocol == "FTP":
		return ftp_delete_file(id, path, filename)
	else:
		return local_delete_file(id, path, filename)

def rename_file(id, path, newpath, filename, newname):
	protocol = get_protocol(id)
	if protocol == "FTP":
		return ftp_rename_file(id, path, newpath, filename, newname)
	else:
		return local_rename_file(id, path, newpath, filename, newname)

def read_file(id, path):
	protocol = get_protocol(id)
	if protocol == "FTP":
		return ftp_read_file(id, path)
	else:
		return local_read_file(id, path)

def list_dir(id, dir = "/"):
	protocol = get_protocol(id)
	if protocol == "FTP":
		return ftp_list_dir(id, dir)
	else:
		return local_list_dir(id, dir)


def list_dir_filter(id, dir = "/", search = ""):
	protocol = get_protocol(id)
	if protocol == "FTP":
		return ftp_list_dir_filter(id, dir, search)
	else:
		return local_list_dir_filter(id, dir, search)
