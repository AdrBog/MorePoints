from flask import session
from io import BytesIO, StringIO
import ftplib
from .misc import *
from .config import *
import ssl
import re

def connect(id):
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

def read_file(id, path):
    ftp = connect(id)
    r = BytesIO()
    ftp.retrbinary(f'RETR /{path}', r.write)
    ftp.quit()
    return r.getvalue()

def list_dir(id, dir = "/"):
    ftp = connect(id)
    ftp.cwd(f'{dir}')
    files = []
    try:
        data = ftp.mlsd(path="", facts=["type", "size", "perm", "modify"])
        files = [f for f in data]
        ftp.quit()
        return files
    except ftplib.error_perm as resp:
        if str(resp) == "550 No files found":
            print("No files in this directory")
            ftp.quit()
            return []
        else:
            ftp.quit()
            return []

def list_dir_filter(id, dir = "/", search = ""):
    files = list_dir(id, dir)
    regex = re.compile(search)
    filter_search = [f for f in files if regex.match(f[0])]
    return filter_search

def list_dir_only_dir(id, dir = "/"):
    files = list_dir(id, dir)
    return [f for f in files if f[1]["type"] == "dir"]

def remove_dir(ftp, path):
    for (name, properties) in ftp.mlsd(path=path):
        if name in ['.', '..']:
            continue
        elif properties['type'] == 'file':
            ftp.delete(f"{path}/{name}")
        elif properties['type'] == 'dir':
            remove_dir(ftp, f"{path}/{name}")
    ftp.rmd(path)
