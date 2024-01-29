from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from utils import *
import json
import os

SITES_DIR = "sites"
HOST = "127.0.0.1"

authorizer = DummyAuthorizer()

sites = ["".join(file.split('.')[0:-1]) for file in os.listdir(SITES_CONFIG_DIR) if file.endswith(".site")]

for site in sites:
    site_config = readJSON(f"{SITES_CONFIG_DIR}/{site}.site")
    if site_config['FTP'].get('Host', HOST) != HOST:
        continue
    authorizer.add_user(site, site_config['FTP']['Password'], site_config['FTP']['Root'], site_config['Permissions']['/'])
    for path, perm in site_config['Permissions'].items():
        try:
            authorizer.override_perm(site, site_config['FTP']['Root'] + path, perm, recursive=True)
        except:
            pass


handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer((HOST, 21), handler)

server.serve_forever()