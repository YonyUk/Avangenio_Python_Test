'''
response

Implementation for the response abstraction for the communication bettwen the server and the client
'''
import json

class BaseResponse:
    '''
    BaseResponse

    base class for the response
    '''
    _attributes = {}

    @property
    def headers(self):
        '''
        the headers inside this response
        '''
        return self._attributes.keys()

    pass

class Response(BaseResponse):

    def __getattr__(self,attr):
        if attr in super()._attributes.keys():
            return super()._attributes[attr]
        return None
    
    def __setattr__(self,attr,value):
        if not type(value) == str:
            raise Exception('value most be string')
        super()._attributes[attr] = value
        pass

    pass