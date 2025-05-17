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
        while count > 0:
            yield self._generate_tokens(self._parse_tree,self._max_length)
            count -= 1
            pass
        pass

    def _generate_tokens(self,tokens,max_length):
        result = []
        for token in tokens:
            length = sum(map(lambda string:len(string),result))
            result.append(self._handle_token(token,max_length-length))
            pass
        return ''.join(result)

    def _handle_token(self,token:tuple,max_length):
        op,value = token
        return self._handlers[op](value,max_length) if op in self._handlers.keys() else ''
    
    def _handle_range(self,value,max_length):
        start,end = value
        return chr(random.randint(start,end))
    
    def _handle_subpattern(self,value,max_length):
        _,_,_,subpattern = value
        return self._generate_tokens(subpattern,max_length)

    def _handle_in(self,value,max_length):
        negate = False
        chars = []
        for item in value:
            if item[0] == NEGATE:
                negate = True
                pass
            else:
                chars.extend(self._expand_item(item,max_length))
                pass
            pass

        if negate:
            valid_chars = set(string.printable).difference(set(chars))
            return random.choice(valid_chars)
        return random.choice(chars)

    def _expand_item(self,item,max_length):
        op,value = item
        return [self._handle_token(item,max_length)]


    def _handle_max_repeat(self,value,max_length):
        min_,max_,subpattern = value
        count = random.randint(min_,min(max_,int(max_length/2.5)))
        return ''.join([self._generate_tokens(subpattern,max_length) for _ in range(count)])
    
    def _handle_branch(self,value,max_length):
        _, subpatterns = value
        chosen = random.choice(subpatterns)
        return ''.join(self._generate_tokens(chosen,max_length))
    
    def _handle_category(self,value,max_length):
        if value == CATEGORY_DIGIT:
            return random.choice(string.digits)
        if value == CATEGORY_WORD:
            return random.choice(string.ascii_letters+string.digits)
        if value == CATEGORY_SPACE:
            return random.choice(string.whitespace)
        return ''
    
    def _handle_any(self,max_length):
        return random.choice(string.printable.replace('\n',''))

    pass