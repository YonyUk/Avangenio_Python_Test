import socket
import threading

class Server:

    def __init__(self,host:str,port:int,max_clients:int):
        self._addr = host,port
        self._server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self._max_clients = max_clients
        self._handlers = {}
        pass

    def _handle_connection(self,connection):
        
        pass

    def run(self):
        self._server.bind(self._addr)
        self._server.listen(self._max_clients)

        while True:
            conn,addr = self._server.accept()
            data = conn.recv(1024)
            print(data)
            pass

        pass

    pass