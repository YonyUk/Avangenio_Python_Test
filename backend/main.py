from server import Server
from service import WordPonderationService
import os
import pathlib
import json

# default values
host = 'localhost'
port = 8080
max_clients = 1

# reading the server config file
for file in os.listdir(os.getcwd()):
    if pathlib.Path(file).name == 'config.json' and pathlib.Path(file).is_file():
        with open(file,'r') as reader:
            data = json.loads(reader.read())
            host = data['HOST']
            port = data['PORT']
            max_clients = data['MAX_CLIENTS']
            pass
        pass
    pass

server = Server(host,port,max_clients)

# adding the services
server['ponderation'] = WordPonderationService

# runing the application
server.run()