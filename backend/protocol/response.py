from protocol.status import Status
'''
response

Implementation for the response abstraction for the communication bettwen the server and the client
'''
import json

class Response(BaseResponse):
    '''
    Response

    response implementation
    '''

    _attributes = {}

    def __init__(self,**headers):
        if not 'Status' in headers.keys():
            raise Exception('<Response> must have a "Status" field')
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
        if attr == 'Status' and type(value) != Status:
            raise Exception("The 'Status' property must be an <enum 'Status'>")
        if attr == 'Body':
            if not type(value) == dict:
                raise Exception("'Body' property most be a dictionary")
            try:
                json.dumps(value)
                pass
            except Exception as ex:
                raise Exception("The 'Body' most be serializable")
        if type(value) != int and type(value) != str:
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

    def headers(self):
        '''
        the headers inside this response
        '''
        return self._attributes.keys()

    pass