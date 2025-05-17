'''
generator

module for the string generation
'''

import string
import random

class StringGenerator:

    _config = {}

    def __init__(self,**config):
        for key in config.keys():
            self._config[key] = config[key]
            pass
        self._sets = {
            'letters':set(string.ascii_letters),
            'letters_lowercase':set(string.ascii_lowercase),
            'letters_uppercase':set(string.ascii_uppercase),
            'digits':set(string.digits),
            'punctuation':set(string.punctuation),
            'printable':set(string.printable),
            'whitespaces':set(string.whitespace)
        }
        pass

    def __getattr__(self,item):
        if item in self._config.keys():
            return self._config[item]
        return None

    def __setattr__(self,item,value):
        self._config[item] = value
        pass

    def GenerateStrings(self,count:int):
        '''
        generate 'counts' strings with the inner specifications

        return an iterable
        '''
        valid_chars = self._config['allowed_chars']
        min_length = self._config['min_length']
        max_length = self._config['max_length']
        string_pattern = self._config['pattern']
        
        chars = self._build_allowed_chars_from_list(valid_chars)

        _count = 0

        while _count < count:
            
            pass
        pass

    def _build_allowed_chars_from_list(self,valid_chars:list):
        '''
        build the set of allowed chars
        '''
        chars = set()
        # if input is not a list, exception is raised
        if not type(valid_chars) == list:
            raise Exception('\'allowed_chars\' field must be a list')
        for allowed in valid_chars:
            # if the current position is a list of characters
            # all characters are added to the set
            if type(allowed) == list:
                # validate that every item is a char
                if not _validate(allowed):
                    raise Exception('Only list of chars are allowed, or the values: letters, letters_lowercase,letters_uppercase,digits,punctuation,printable or whitespaces')
                chars = chars.union(set(allowed))
                pass
            elif type(allowed) == str:
                # if the value is known
                if allowed in self._sets.keys():
                    chars = chars.union(self._sets[allowed])
                    pass
                else:
                    raise Exception(f'Unknown option {allowed}')
                pass
            else:
                raise Exception('Only strings or list of chars are allowed for the elements of \'allowed_chars\' field')
            pass
        return chars

    pass

def _validate(chars:list):
    for c in chars:
        if type(c) != str or len(c) != 1:
            return False
        pass
    return True

# generator = StringGenerator(
#     allowed_chars=['printable'],
#     min_length=50,
#     max_length=100,
#     pattern='\S+[ ]'*3+'\S+[ ]?'*2+'\S+'
# )
