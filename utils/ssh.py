"""
This module contains methods for connecting and executing file actions on an SSH server.
"""
from flask import jsonify
from io import BytesIO, StringIO
from .misc import *
from .config import *
import paramiko
import time
import re
import stat

def ssh_connect(id):
    ssh_data = read_point_config(id)
    HOST = ssh_data["SSH"].get("Host", '127.0.0.1')
    PORT = ssh_data["SSH"].get("Port", '22')
    USER = ssh_data["SSH"].get("User", '')
    PASS = ssh_data["SSH"].get("Password", '')
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=HOST,port=PORT,username=USER,password=PASS)
    sftp = ssh_client.open_sftp()
    return sftp

def ssh_create_folder(id, path, filename):
    with ssh_connect(id) as sftp:
        try:
            output = sftp.mkdir(f"./{path}/{filename}")
            return jsonify(status="Ok", output=output)
        except Exception as error:
            return jsonify(status="Error", output=str(error))

def ssh_create_file(id, path, filename, content):
    with ssh_connect(id) as sftp:
        try:
            with sftp.open(f"./{path}/{filename}", "wb") as file:
                output = file.write(content.encode())
                return jsonify(status="Ok", output=output)
        except Exception as error:
            return jsonify(status="Error", output=str(error))

def ssh_upload_file(id, path, files):
    with ssh_connect(id) as sftp:
        try:
            for file in files:
                with sftp.open(f"./{path}/{file.filename}", "wb") as f:
                    output = f.write(file.read())
            return output
        except Exception as error:
            return jsonify(status="Error", output=str(error))

def ssh_delete_file(id, path, filename):
    with ssh_connect(id) as sftp:
        try:
            fileattr = sftp.lstat(f"./{path}/{filename}")
            if stat.S_ISDIR(fileattr.st_mode):
                output = sftp.rmdir(f"./{path}/{filename}")
            else:
                output = sftp.remove(f"./{path}/{filename}")
            return jsonify(status="Ok", output=output)
        except Exception as error:
            return jsonify(status="Error", output=str(error))

def ssh_rename_file(id, path, newpath, filename, newname):
    with ssh_connect(id) as sftp:
        try:
            output = sftp.posix_rename(f"./{path}/{filename}", f"./{newpath}/{newname}")
            return jsonify(status="Ok", output=output)
        except Exception as error:
            return jsonify(status="Error", output=str(error))

def ssh_read_file(id, path):
    with ssh_connect(id) as sftp:
        with sftp.open(f"./{path}") as file:
            return file.read()

def ssh_list_dir(id, dir):
    with ssh_connect(id) as sftp:
        files = []
        try:
            for f in sftp.listdir_attr(f"./{dir}"):
                files.append([f.filename, {
                    "size": f.st_size,
                    "modify": time.ctime(f.st_mtime),
                    "type": "dir" if stat.S_ISDIR(f.st_mode) else "file"
                }])
        except Exception as error:
            print(error)
        finally:
            return files
