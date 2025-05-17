'''
appconfig
'''

from configurable import Configurable
from core import StringGenerator

class AppConfig(Configurable):
    '''
    app cofiguration implementation
    ''' 
    
    def __init__(self,**kwargs):
        if not 'Generator' in kwargs.keys():
            raise Exception('No given value for the param \'Generator\'')
        if not isinstance(kwargs['Generator'],StringGenerator):
            raise ValueError('The value of param \'Generator\' must be a StringGenerator-like object')
        super().__init__(**kwargs)
        pass

    pass