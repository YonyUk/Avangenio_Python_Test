'''
ponderation service

service for the word's ponderations
'''
from .service import Service
from protocol import ServerOperation,Request,Status
import re

def ponderation_function(request:Request):
    data = request.Body['text']
    total_pattern = '\S'
    digits_pattern = '\d'
    whitespace_pattern = '\s'
    digits_count = len(re.findall(digits_pattern,data))
    whitespace_count = len(re.findall(whitespace_pattern,data))
    chars_count = len(re.findall(total_pattern,data)) - digits_count
    return {
        'Status':Status.OK,
        'Status Message':'OK',
        'Body':{
            'value':(chars_count * 1.5 + digits_count * 2)/whitespace_count
        }
    }

WordPonderationService = Service()
WordPonderationService.AddHandler(ServerOperation.PONDERATION,ponderation_function)