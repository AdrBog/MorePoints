"""
This module controls the connections between the client and the server, regardless of the protocol being used.

To see each protocol independently, watch utils.ftp, utils.ssh, utils.webdav or utils.local.
"""
from .ftp import *
from .local import *
from .webdav import *
from .ssh import *
from flask import redirect

def get_protocol(id):
	point_data = read_point_config(id)
	connection = point_data.get("Connection", {})
	return connection.get("Protocol", "FTP")

def connect(id):
	protocol = get_protocol(id)
	protocol_functions = {
		"FTP": ftp_connect,
		"SSH": ssh_connect,
		"WebDav": webdav_connect
	}
	return protocol_functions.get(protocol)(id)

def create_folder(id, path, filename):
	protocol = get_protocol(id)
	protocol_functions = {
		"FTP": ftp_create_folder,
		"SSH": ssh_create_folder,
		"Local" : local_create_folder
	}
	return protocol_functions.get(protocol, "Local")(id, path, filename)

def create_file(id, path, filename, content):
	protocol = get_protocol(id)
	protocol_functions = {
		"FTP": ftp_create_file,
		"SSH": ssh_create_file,
		"Local" : local_create_file
	}
	return protocol_functions.get(protocol, "Local")(id, path, filename, content)

def upload_file(id, path, files):
	protocol = get_protocol(id)
	protocol_functions = {
		"FTP": ftp_upload_file,
		"SSH": ssh_upload_file,
		"Local" : local_upload_file
	}
	return protocol_functions.get(protocol, "Local")(id, path, files)

def delete_file(id, path, filename):
	protocol = get_protocol(id)
	protocol_functions = {
		"FTP": ftp_delete_file,
		"SSH": ssh_delete_file,
		"Local" : local_delete_file
	}
	return protocol_functions.get(protocol, "Local")(id, path, filename)

def rename_file(id, path, newpath, filename, newname):
	protocol = get_protocol(id)
	protocol_functions = {
		"FTP": ftp_rename_file,
		"SSH": ssh_rename_file,
		"Local" : local_rename_file
	}
	return protocol_functions.get(protocol, "Local")(id, path, newpath, filename, newname)

def read_file(id, path):
	protocol = get_protocol(id)
	protocol_functions = {
		"FTP": ftp_read_file,
		"SSH": ssh_read_file,
		"WebDav": webdav_read_file,
		"Local" : local_read_file
	}
	return protocol_functions.get(protocol, "Local")(id, path)

def list_dir(id, dir = "/"):
	protocol = get_protocol(id)
	protocol_functions = {
		"FTP": ftp_list_dir,
		"SSH": ssh_list_dir,
		"WebDav": webdav_list_dir,
		"Local" : local_list_dir
	}
	return protocol_functions.get(protocol, "Local")(id, dir)

def list_dir_filter(id, dir = "/", search = ""):
	files = list_dir(id, dir)
	regex = re.compile(search)
	filter_search = [f for f in files if regex.match(f[0])]
	return filter_search
