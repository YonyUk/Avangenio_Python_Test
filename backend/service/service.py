'''
service

Definitions for implementations of a server service
'''

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from protocol import ServerOperation,Request,Status

class Service:
    '''
    Service

    base service implementation
    '''

    _handlers = {}

    @property
    def services(self):
        for key in self._handlers.keys():
            yield key,self._handlers[key]
        pass

    def AddHandler(self,operation:ServerOperation,handler):
        '''
        handler: function that will response to the specified operation, the input argument must be <Request> type
        '''
        if type(operation) != ServerOperation:
            raise Exception("'operation' must be member of <enum 'ServerOperation'>")
        self._handlers[operation] = handler

    def Handle(self,request:Request):
        return self._handlers[request.Operation](request)
    
    def configure(self,**kwargs):
        raise NotImplementedError()

    pass