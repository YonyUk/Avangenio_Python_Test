'''
request

Implementation for the request abstraction for the communication bettwen the server and the client
'''
import json
from .server_operation import ServerOperation

class Request:
    
    '''
    Request

    request implementation
    '''
    _attributes = {}

    def __init__(self,**headers):
        if 'Status' in headers.keys():
            raise Exception('<Request> has not a "Status" field')
        if not 'Operation' in headers.keys():
            raise Exception('<Request> must have a "Operation" field')
        if not headers['Operation'] in [op for op in ServerOperation]:
            raise Exception('"Operation" field must be a <enum ServerOperation> member')
        for key in headers.keys():
            self._attributes[key] = headers[key]
            pass
        pass

    def __getattr__(self,attr):
        if attr == 'headers':
            return self.headers()
        if attr in self._attributes.keys():
            return self._attributes[attr]
        return None
    
    def __setattr__(self,attr,value):
        if attr == 'headers':
            raise Exception("Field 'headers' is readonly")
        if attr == 'Status':
            raise Exception("There's not exists the property 'Status' for this class")
        if attr == 'Body':
            if not type(value) == dict:
                raise Exception("'Body' property most be a dictionary")
            try:
                json.dumps(value)
                pass
            except Exception as ex:
                raise Exception("The 'Body' most be serializable")
        elif type(value) != int and type(value) != str:
            raise Exception("All the properties most be serializables")
        self._attributes[attr] = value
        pass

    def __str__(self):
        result = '{\n'
        for key in self.headers():
            result += f'\t{key}:{self._attributes[key]}\n'
            pass
        return result + '}'

    def __repr__(self):
        return str(self)
    
    def to_dict(self):
        '''
        return a dictionary representation of this request
        '''
        return self._attributes

    def headers(self):
        '''
        the headers inside this request
        '''
        return self._attributes.keys()

    pass