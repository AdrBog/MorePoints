from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from utils.misc import *
import json
import os

HOST = "127.0.0.1"

authorizer = DummyAuthorizer()

ftp_users = readJSON(f"{CONFIG_DIR}/ftp_users.json")

for user in ftp_users:
    authorizer.add_user(user["name"], user["password"], user["root"], user["perm"])

handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer((HOST, 21), handler)

server.serve_forever()
