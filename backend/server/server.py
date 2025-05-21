'''
server
'''
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import socket
import threading
from protocol import ServerOperation,Request,Status
from tools import serialize,dserialize,sendto
from service import Service
import time
import json
import logging

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s [%(threadName)s] %(levelname)s: %(message)s')

class Server:
    '''
    Server

    server implementation
    '''
    _services = {}
    _addr = None
    _server = None
    _max_clients = 1
    _buffer_size = 1024
    
    def __init__(self,host:str,port:int,**server_options):
        if type(host) != str:
            raise Exception('host must be string')
        if type(port) != int:
            raise Exception('port must be integer')
        self._addr = host,port
        self._server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        if 'max_clients' in server_options.keys():
            if type(server_options['max_clients']) != int:
                raise Exception('max_clients must be integer')
            self._max_clients = server_options['max_clients']
            pass
        if 'buffer_size' in server_options.keys():
            if type(server_options['buffer_size']) != int or server_options['buffer_size'] < 1:
                raise ValueError('<buffer_size> property must be an integer greather than 0')
            self._buffer_size = server_options['buffer_size']
            pass
        self._services = {}
        self._clients_process = []
        threading.Thread(target=self._kill_deads_clients_threads,daemon=True,name="Thread Cleaner").start()
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
                'StatusMessage':msg
            }
        try:
            for service in self._services.values():
                operations = [s[0] for s in service.services]
                if request.Operation in operations:
                    return service.Handle(request)
                pass
            pass
        except Exception as ex:
            return {
                'Status':Status.ERROR,
                'StatusMessage':f'{ex}'
            }
        return {
            'Status':Status.ERROR,
            'StatusMessage':f'No handler implemented for operation <{request.Operation}>'
        }

    def _process_client_in_background(self,conn:socket.socket):
        request = conn.recv(self._buffer_size)
        while True:
            try:
                request = Request(**dserialize(request))
                break
            except Exception as ex:
                request += conn.recv(self._buffer_size)
                pass
            pass
        
        response = self._handle_request(request)
        conn.sendall(serialize(**response))           
        conn.close()
        pass

    def _kill_deads_clients_threads(self):
        while True:
            deads_threads = [t for t in self._clients_process if not t.is_alive()]
            self._clients_process = [t for t in self._clients_process if t.is_alive()]
            for t in deads_threads:
                t.join()
                pass
            time.sleep(0.5)
            pass


    def run(self):
        '''
        run the server
        '''
        self._server.bind(self._addr)
        self._server.listen(self._max_clients)

        logging.info(f'server running at {self._addr}')
        logging.info(f'max clients allowed in concurrency: {self._max_clients}')
        logging.info(f'buffer size: {self._buffer_size}')
        while True:
            conn,addr = self._server.accept()
            thread = threading.Thread(name=f"client at {addr} request process",target=self._process_client_in_background,daemon=True,args=(conn,))
            thread.start()        
            self._clients_process.append(thread)
            pass

        pass

    def __setitem__(self,item:str,value:Service):
        if type(item) != str:
            raise Exception("Must be indexed over strings")
        if not isinstance(value,Service):
            raise Exception("The given value must be a Service's class instance")
        self._services[value] = value
        if os.path.exists(f'{item}Config.json'):
            with open(f'{item}Config.json','r') as reader:
                config = json.loads(reader.read())
                value.configure(**config)
                pass
            pass
        else:
            raise Exception(f'No configuration file given for <{item}> service: "{item}Config.json" file is required at {os.getcwd()}')
        pass

    def __getitem__(self,item:str):
        if type(item) != str:
            raise Exception("Expected a string")
        return self._services[item]

    def __delitem__(self,item:str):
        if type(item) != str:
            raise Exception("Expected a string")
        del self._services[item]
        pass

    pass