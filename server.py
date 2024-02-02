from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from utils.misc import *
import json
import os

HOST = "127.0.0.1"

authorizer = DummyAuthorizer()

points = ["".join(file.split('.')[0:-1]) for file in os.listdir(POINTS_CONFIG_DIR) if file.endswith(".point")]

for point in points:
    point_config = readJSON(f"{POINTS_CONFIG_DIR}/{point}.point")
    if point_config['FTP'].get('Host', HOST) != HOST:
        continue
    authorizer.add_user(point, point_config['FTP']['Password'], point_config['FTP']['Root'], point_config['Permissions']['/'])
    for path, perm in point_config['Permissions'].items():
        try:
            authorizer.override_perm(point, point_config['FTP']['Root'] + path, perm, recursive=True)
        except:
            pass


handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer((HOST, 21), handler)

server.serve_forever()
