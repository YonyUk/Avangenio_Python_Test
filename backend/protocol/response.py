from protocol.status import Status
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

    def headers(self):
        '''
        the headers inside this response
        '''
        return self._attributes.keys()

    pass

class Response(BaseResponse):
    '''
    Response

    response implementation
    '''

    def __init__(self,**headers):
        if not 'Status' in headers.keys():
            raise Exception('<Response> must have a "Status" field')
        for key in headers.keys():
            super()._attributes[key] = headers[key]
            pass
        pass

    def __getattr__(self,attr):
        if attr == 'headers':
            return super().headers()
        if attr in super()._attributes.keys():
            return super()._attributes[attr]
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
        super()._attributes[attr] = value
        pass

    def __str__(self):
        result = '{\n'
        for key in super().headers():
            result += f'\t{key}:{self._attributes[key]}\n'
            pass
        return result + '}'

    def __repr__(self):
        return str(self)

    pass