from server import Server
from service import WordPonderationService

server = Server('localhost',8080,1)
server['ponderation'] = WordPonderationService

server.run()