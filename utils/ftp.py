from io import BytesIO, StringIO
import ftplib
from .misc import *
from .config import *

def connect(id):
    ftp_data = read_site_config(id)
    ftp = ftplib.FTP(ftp_data["FTP"].get("Host", '127.0.0.1'))
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
