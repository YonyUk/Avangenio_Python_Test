'''
regex generator

module to generate strings from a regular expression
'''

import re
import random
import string
import sre_parse
from sre_constants import *

class RegexGenerator:
    '''
    regex generator

    class that generate strings from a regular expression
    '''

    def __init__(self,pattern:str,min_length=10,max_length=20):
        self._parse_tree = sre_parse.parse(pattern)
        self._max_length = max_length
        self._min_length = min_length
        self._handlers = {
            LITERAL:lambda value,max_length:chr(value),
            IN:self._handle_in,
            RANGE:self._handle_range,
            MAX_REPEAT:self._handle_max_repeat,
            SUBPATTERN:self._handle_subpattern,
            BRANCH:self._handle_branch,
            CATEGORY:self._handle_category,
            ANY:lambda value,max_length:self._handle_any()
        }
        pass

    def Generate(self,count:int):
        '''
        generate 'count' strings with the internal pattern given
        '''
        while count > 0:
            yield self._generate_tokens(self._parse_tree,self._max_length)
            count -= 1
            pass
        pass

    def _generate_tokens(self,tokens,max_length):
        result = []
        for token in tokens:
            # claculate the length of the total string
            length = sum(map(lambda string:len(string),result))
            # adds a new token generated to the result
            result.append(self._handle_token(token,max_length-length))
            pass
        # return the concatenation of all the tokens
        return ''.join(result)

    def _handle_token(self,token:tuple,max_length):
        # gets the regex op and the value
        op,value = token
        # return the result for the given token
        return self._handlers[op](value,max_length) if op in self._handlers.keys() else ''
    
    def _handle_range(self,value,max_length):
        # return a random char from the given range
        start,end = value
        return chr(random.randint(start,end))
    
    def _handle_subpattern(self,value,max_length):
        # generate a token with the given subpattern
        _,_,_,subpattern = value
        return self._generate_tokens(subpattern,max_length)

    def _handle_in(self,value,max_length):
        negate = False
        chars = []
        # checks if the set of values is negated
        for item in value:
            if item[0] == NEGATE:
                negate = True
                pass
            else:
                # expand the item
                chars.extend(self._expand_item(item,max_length))
                pass
            pass

        if negate:
            # if negate, return a char that is not in the given set
            valid_chars = set(string.printable).difference(set(chars))
            return random.choice(valid_chars)
        # return a random choice from the given set
        return random.choice(chars)

    def _expand_item(self,item,max_length):
        op,value = item
        # expand an item
        return [self._handle_token(item,max_length)]


    def _handle_max_repeat(self,value,max_length):
        # generate a token with the length nt greather than the max_length
        min_,max_,subpattern = value
        count = random.randint(min_,min(max_,int(max_length/2.5)))
        return ''.join([self._generate_tokens(subpattern,max_length) for _ in range(count)])
    
    def _handle_branch(self,value,max_length):
        # return a choice from a set of posibles patterns
        _, subpatterns = value
        chosen = random.choice(subpatterns)
        return ''.join(self._generate_tokens(chosen,max_length))
    
    def _handle_category(self,value,max_length):
        # return a token from the given category
        if value == CATEGORY_DIGIT:
            return random.choice(string.digits)
        if value == CATEGORY_WORD:
            return random.choice(string.ascii_letters+string.digits)
        if value == CATEGORY_SPACE:
            return random.choice(string.whitespace)
        return ''
    
    def _handle_any(self,max_length):
        # return any character different to jump line
        return random.choice(string.printable.replace('\n',''))

    pass