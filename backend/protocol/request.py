'''
request

Implementation for the request abstraction for the communication bettwen the server and the client
'''
import json

class BaseRequest:
    '''
    BaseRequest

    base class for the request
    '''
    _attributes = {}

    @property
    def headers(self):
        '''
        the headers inside this request
        '''
        return self._attributes.keys()

    pass

class Request(BaseRequest):
    
    '''
    Request

    request implementation
    '''

    def __getattr__(self,attr):
        if attr in super()._attributes.keys():
            return super()._attributes[attr]
        return None
    
    def __setattr__(self,attr,value):
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
        if type(value) != int and type(value) != str:
            raise Exception("All the properties most be serializables")
        super()._attributes[attr] = value
        pass

    pass