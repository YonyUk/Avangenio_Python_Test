'''
ponderation service

service for the word's ponderations
'''
from .service import Service
from protocol import ServerOperation,Request,Status
import re
import logging

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s [%(threadName)s] %(levelname)s: %(message)s')

def ponderation_function(request:Request):
    # geting the data
    data = request.Body['text']
    # pattern of the text
    total_pattern = '\S'
    digits_pattern = '\d'
    whitespace_pattern = '\s'
    
    special_pattern = 'aa|aA|Aa|AA'

    if re.search(special_pattern,data) != None:
        logging.info(f"Double 'a' rule detected >>> {data}")
        return {
            'Status':Status.OK,
            'StatusMessage':'OK',
            'Body':{
                'value':1000
            }
        }
    if not check_string(data):
        return {
            'Status':Status.ERROR,
            'StatusMessage':'detected string with bad pattern'
        }
    
    digits_count = len(re.findall(digits_pattern,data))
    whitespace_count = len(re.findall(whitespace_pattern,data))
    chars_count = len(re.findall(total_pattern,data)) - digits_count
        
    return {
        'Status':Status.OK,
        'StatusMessage':'OK',
        'Body':{
            'value':(chars_count * 1.5 + digits_count * 2)/whitespace_count
        }
    }

def check_string(string:str):
    if len(string) < 50 and len(string) > 100: return False
    pattern = '[a-zA-Z0-9]+[ ]?'*5 + '[a-zA-Z0-9]+'
    return re.fullmatch(pattern,string) != None

WordPonderationService = Service()
WordPonderationService.AddHandler(ServerOperation.PONDERATION,ponderation_function)