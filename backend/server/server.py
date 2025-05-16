'''
server
'''
import socket
import threading
from protocol import ServerOperation,ToRequest,Request
from tools import serialize,dserialize

class Server:
    '''
    Server

    server implementation
    '''

    def __init__(self,host:str,port:int,max_clients:int):
        self._addr = host,port
        self._server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self._max_clients = max_clients
        self._handlers = {}
        pass

    def _handle_request(self,request:Request):
        print(request)
        pass

    def run(self):
        '''
        run the server
        '''
        self._server.bind(self._addr)
        self._server.listen(self._max_clients)

        while True:
            conn,_ = self._server.accept()
            request = ToRequest(**dserialize(conn.recv(1024)))
            self._handle_request(request)
            conn.close()
            pass

        pass

    def __setitem__(self,item:ServerOperation,value):
        if type(item) != ServerOperation:
            raise Exception("Expected a member of <enum 'ServerOperation'>")
        self._handlers[item] = value
        pass

    def __getitem__(self,item:ServerOperation):
        if type(item) != ServerOperation:
            raise Exception("Expected a member of <enum 'ServerOperation'>")
        return self._handlers[item]

    def __delitem__(self,item:ServerOperation):
        if type(item) != ServerOperation:
            raise Exception("Expected a member of <enum 'ServerOperation'>")
        del self._handlers[item]

    pass