from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import configparser
from sites import *
from app import CONFIG_DIR, sites_config

SITES_DIR = "sites"

authorizer = DummyAuthorizer()

for site in sites_config.sections():
    authorizer.add_user(site, sites_config.get(site, "password"), sites_config.get(site, "root"), perm=sites_config.get(site, "perm"))

handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer(("127.0.0.1", 21), handler)

server.serve_forever()