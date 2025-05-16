'''
server
'''
import socket
import threading
from protocol import ServerOperation,ToRequest,Request,ToResponse,Status
from tools import serialize,dserialize
from service import Service

class BaseServer:
    _services = {}
    _addr = None
    _server = None
    _max_clients = 0
    
    def __init__(self,host:str,port:int,max_clients:int):
        if type(host) != str:
            raise Exception('host must be string')
        if type(port) != int:
            raise Exception('port must be integer')
        if type(max_clients) != int:
            raise Exception('max_clients must be integer')
        self._addr = host,port
        self._server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self._max_clients = max_clients
        self._services = {}
        pass
    
    def _filt_request(self,request:Request):
        if request.Operation == None:
            return False,'Bad formed request: No <Operation> header found'
        return True,'OK'

    def _handle_request(self,request:Request):
        check,msg = self._filt_request(request)
        if not check:
            return {
                'Status': Status.ERROR,
                'Status Message':msg
            }
        for service in self._services.values():
            operations = [s[0] for s in service.services]
            if request.Operation in operations:
                return service.Handle(request)
            pass
        return {
            'Status':Status.ERROR,
            'Status Message':f'No handler implemented for operation <{request.Operation}>'
        }

    def run(self):
        '''
        run the server
        '''
        self._server.bind(self._addr)
        self._server.listen(self._max_clients)

        while True:
            conn,_ = self._server.accept()
            request = ToRequest(**dserialize(conn.recv(1024)))
            response = self._handle_request(request)
            conn.sendall(serialize(**response))           
            conn.close()
            pass

        pass

    pass

class Server(BaseServer):
    '''
    Server

    server implementation
    '''

    def __init__(self,host:str,port:int,max_clients:int):
        super().__init__(host,port,max_clients)
        pass

    def __setitem__(self,item:str,value:Service):
        if type(item) != str:
            raise Exception("Must be indexed over strings")
        if not isinstance(value,Service):
            raise Exception("The given value must be a Service's class instance")
        self._services[value] = value

    def __getitem__(self,item:str):
        if type(item) != str:
            raise Exception("Expected a string")
        return self._services[item]

    def __delitem__(self,item:str):
        if type(item) != str:
            raise Exception("Expected a string")
        del self._services[item]

    pass