# The same file as server.py but with TLS/SSL Support
# You will need to install pyopenssl with pip
# And generate the certfile and the keyfile with openssl

from OpenSSL import SSL
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import TLS_FTPHandler
from pyftpdlib.servers import FTPServer
from utils.misc import *
import json
import os

HOST = "127.0.0.1"

authorizer = DummyAuthorizer()

ftp_users = readJSON(f"{CONFIG_DIR}/ftp_users.json")

for user in ftp_users:
    authorizer.add_user(user["name"], user["password"], user["root"], user["perm"])

handler = TLS_FTPHandler

# CHANGE THESE TO THE CURRENT FILE LOCATIONS
handler.certfile = 'venv/cert.pem' 
handler.keyfile = 'venv/key.pem'

handler.authorizer = authorizer

server = FTPServer((HOST, 21), handler)

server.serve_forever()
