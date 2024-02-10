from flask import session
from io import BytesIO, StringIO
import ftplib
from .misc import *
from .config import *

def connect(id):
    ftp_data = read_point_config(id)
    HOST = ftp_data["FTP"].get("Host", '127.0.0.1')
    PORT = int(ftp_data["FTP"].get("Port", '21'))
    USE_TLS = ftp_data["FTP"].get("TLS", 'disabled') == 'active'
    if (USE_TLS):
        ftp = ftplib.FTP_TLS()
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

def remove_dir(ftp, path):
    for (name, properties) in ftp.mlsd(path=path):
        if name in ['.', '..']:
            continue
        elif properties['type'] == 'file':
            ftp.delete(f"{path}/{name}")
        elif properties['type'] == 'dir':
            remove_dir(ftp, f"{path}/{name}")
    ftp.rmd(path)
