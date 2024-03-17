"""
This module contains methods for connecting and executing file actions on an FTP server. 
"""
from flask import session, jsonify
from io import BytesIO, StringIO
import ftplib
from .misc import *
from .config import *
import ssl
import re

def ftp_connect(id):
    ftp_data = read_point_config(id)
    HOST = ftp_data["FTP"].get("Host", '127.0.0.1')
    PORT = int(ftp_data["FTP"].get("Port", '21'))
    USE_TLS = ftp_data["FTP"].get("TLS", 'disabled') == 'active'
    if (USE_TLS):
        ftp = ftplib.FTP_TLS()
        ftp.ssl_version = ssl.PROTOCOL_SSLv23
        ftp.connect(HOST, PORT)
        ftp.login(ftp_data["FTP"].get("User", id), ftp_data["FTP"]["Password"])
        ftp.prot_p()
        return ftp
    ftp = ftplib.FTP()
    ftp.connect(HOST, PORT)
    ftp.login(ftp_data["FTP"].get("User", id), ftp_data["FTP"]["Password"])
    return ftp

def ftp_create_folder(id, path, filename):
    with ftp_connect(id) as ftp:
        try:
            output = ftp.mkd(f"{path}/{filename}")
            return jsonify(status="Ok", output=output)
        except ftplib.all_errors as error:
            return jsonify(status="Error", output=str(error))

def ftp_create_file(id, path, filename, content):
    with ftp_connect(id) as ftp:
        try:
            output = ftp.storbinary(f'STOR {path}/{filename}', BytesIO(content.encode()))
            return jsonify(status="Ok", output=output)
        except ftplib.all_errors as error:
            return jsonify(status="Error", output=str(error))

def ftp_upload_file(id, path, files):
    with ftp_connect(id) as ftp:
        try:
            ftp.cwd(path)
            for f in files:
                output = ftp.storbinary('STOR ' + f.filename, f)
            return jsonify(status="Ok", output=output)
        except ftplib.all_errors as error:
            return jsonify(status="Error", output=str(error))

def ftp_delete_file(id, path, filename):
    with ftp_connect(id) as ftp:
        try:
            try:
                output = ftp.delete(f"{path}/{filename}")
            except ftplib.error_perm as error:
                if error.args[0][:3] == "550": # 505: Is a directory
                    output = ftp_remove_dir(ftp, f"{path}/{filename}")
            return jsonify(status="Ok", output=output)
        except ftplib.all_errors as error:
            return jsonify(status="Error", output=str(error))

def ftp_rename_file(id, path, newpath, filename, newname):
    with ftp_connect(id) as ftp:
        try:
            for file in ftp.nlst(newpath):
                if file == newname:
                    return jsonify(status="Error", output=Error.FILE_EXISTS)
            output = ftp.rename(f"{path}/{filename}", f"{newpath}/{newname}")
            return jsonify(status="Ok", output=output)
        except ftplib.all_errors as error:
            return jsonify(status="Error", output=str(error))

def ftp_read_file(id, path):
    with ftp_connect(id) as ftp:
        r = BytesIO()
        ftp.retrbinary(f'RETR /{path}', r.write)
        return r.getvalue()

def ftp_list_dir(id, dir = "/"):
    with ftp_connect(id) as ftp:
        ftp.cwd(f'{dir}')
        files = []
        try:
            data = ftp.mlsd(path="", facts=["type", "size", "perm", "modify"])
            files = [f for f in data]
            return files
        except ftplib.error_perm as resp:
            if str(resp) == "550 No files found":
                print("No files in this directory")
            return []

def ftp_remove_dir(ftp, path):
    for (name, properties) in ftp.mlsd(path=path):
        if name in ['.', '..']:
            continue
        elif properties['type'] == 'file':
            ftp.delete(f"{path}/{name}")
        elif properties['type'] == 'dir':
            remove_dir(ftp, f"{path}/{name}")
    ftp.rmd(path)
