from server import Server
from service import WordPonderationService,SpecificationsService
import os
import pathlib
import json

# default values
host = 'localhost'
port = 8080

config = {}

# reading the server config file
for file in os.listdir(os.getcwd()):
    if pathlib.Path(file).name == 'config.json' and pathlib.Path(file).is_file():
        with open(file,'r') as reader:
            data = json.loads(reader.read())
            if 'HOST' in data.keys():
                host = data['HOST']
                pass
            if 'PORT' in data.keys():
                port = data['PORT']
                pass
            config = data
            pass
        pass
    pass

server = Server(host,port,**config)

# adding the services
server['ponderation'] = WordPonderationService
server['specifications'] = SpecificationsService(**config)

# runing the application
server.run()