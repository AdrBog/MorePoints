from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from sites import *
from app import CONFIG_DIR
import json

SITES_DIR = "sites"

authorizer = DummyAuthorizer()

with open(f"{CONFIG_DIR}/sites.json", "r") as sites:
    for key, site in json.load(sites).items():
        authorizer.add_user(key, site['password'], site['root'], perm=site['perm'])
        if 'extra_perm' in site:
            for folder, perm in site['extra_perm'].items():
                try:
                    authorizer.override_perm(key, site['root'] + folder, perm, recursive=True)
                except:
                    pass


handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer(("127.0.0.1", 21), handler)

server.serve_forever()