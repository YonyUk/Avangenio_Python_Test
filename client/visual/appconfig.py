'''
appconfig

configuration for the visual side
'''

from configurable import Configurable

class AppConfig(Configurable):
    '''
    app cofiguration implementation
    ''' 
    
    def __init__(self,**kwargs):
        if not 'pattern' in kwargs.keys():
            raise Exception('No given value for the param \'pattern\'')
        if type(kwargs['pattern']) != str:
            raise ValueError('The value of param \'pattern\' must be str')
        if not 'min_chars' in kwargs.keys():
            raise Exception('No given value for the param \'min_chars\'')
        if not 'max_chars' in kwargs.keys():
            raise Exception('No given value for the param \'max_chars\'')
        if type(kwargs['min_chars']) != int:
            raise ValueError('The value of param \'min_chars\' must be int')
        if type(kwargs['max_chars']) != int:
            raise ValueError('The value of param \'max_chars\' must be int')
        if not 'host' in kwargs.keys():
            raise Exception('No given value for the param \'host\'')
        if not 'port' in kwargs.keys():
            raise Exception('No given value for the param \'port\'')
        if type(kwargs['host']) != str:
            raise ValueError('The value of param \'host\' must be str')
        if type(kwargs['port']) != int:
            raise ValueError('The value of param \'port\' must be int')
        super().__init__(**kwargs)
        pass

    pass