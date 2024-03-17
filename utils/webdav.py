"""
TODO: WEBDAV IS INCOMPLETE
This module contains methods for connecting and executing file actions on an WebDev server.
"""
from webdav3.client import Client
from io import BytesIO, StringIO
from .misc import *
from .config import *
import re

def webdav_connect(id):
    webdav_data = read_point_config(id)
    HOST = webdav_data["WebDav"].get("Host", '127.0.0.1')
    USER = webdav_data["WebDav"].get("User", '')
    PASS = webdav_data["WebDav"].get("Password", '')
    webdav = Client({
    	'webdav_hostname': HOST,
        'webdav_login':    USER,
        'webdav_password': PASS
    })
    return webdav

def webdav_read_file(id, path):
    webdav = webdav_connect(id)
    file = webdav.resource(path)
    r = BytesIO()
    file.write_to(r)
    return r.getvalue()

def webdav_list_dir(id, dir):
    webdav = webdav_connect(id)
    files = []
    try:
        for f in webdav.list(dir):
            file_stats = webdav.info(f"{dir}/{f}")
            files.append([f, {
                "size": file_stats.get('size'),
                "modify": file_stats.get('modified'),
                "type": "dir" if file_stats.get('content_type') in ["httpd/unix-directory"] else "file"
            }])
    except Exception as error:
        print(error)
    finally:
        return files
    
