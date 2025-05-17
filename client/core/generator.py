'''
generator

module for the string generation
'''

import string
import random
from core.regex_generator import RegexGenerator
from configurable import Configurable

class StringGenerator(Configurable):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        pass

    def GenerateStrings(self,count:int):
        '''
        generate 'counts' strings with the inner specifications

        return an iterable
        '''
        min_length = self._attributes['min_length']
        max_length = self._attributes['max_length']
        string_pattern = self._attributes['pattern']
        
        gen = RegexGenerator(string_pattern,min_length,max_length)
        for word in gen.Generate(count):
            yield word
        pass

    pass

def _validate(chars:list):
    for c in chars:
        if type(c) != str or len(c) != 1:
            return False
        pass
    return True