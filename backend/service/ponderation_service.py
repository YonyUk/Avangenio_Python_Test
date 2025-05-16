'''
ponderation service

service for the word's ponderations
'''
from .service import Service
from protocol import ServerOperation,Request,Status
import re
import logging
import datetime

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s [%(threadName)s] %(levelname)s: %(message)s')

def ponderation_function(request:Request):
    # geting the data
    data = request.Body['text'].split('\n')
    start = datetime.datetime.now()
    values = {}

    for line in data:
        if not check_string(line):
            return {
                'Status':Status.ERROR,
                'StatusMessage':'detected string with bad pattern'
            }
        values[line] = get_word_ponderation(line)
        pass
    t = datetime.datetime.now() - start
    logging.info(f'Process completed in {t}')
    return {
        'Status':Status.OK,
        'StatusMessage':'OK',
        'Body':{
            'result':values
        }
    }

def get_word_ponderation(string:str):
    # pattern of the text
    total_pattern = '\S'
    digits_pattern = '\d'
    whitespace_pattern = '\s'
    
    special_pattern = 'aa|aA|Aa|AA'

    if re.search(special_pattern,string) != None:
        logging.info(f"Double 'a' rule detected >>> {string}")
        return 1000
    digits_count = len(re.findall(digits_pattern,string))
    whitespace_count = len(re.findall(whitespace_pattern,string))
    chars_count = len(re.findall(total_pattern,string)) - digits_count
    result = (chars_count * 1.5 + digits_count * 2)/whitespace_count
    logging.info(f'numbers: {digits_count}, whitespaces: {whitespace_count}, letters: {chars_count}, ponderation: {result}')
    return result

def check_string(string:str):
    if len(string) < 50 and len(string) > 100: return False
    pattern = '[a-zA-Z0-9]+[ ]?'*5 + '[a-zA-Z0-9]+'
    return re.fullmatch(pattern,string) != None

WordPonderationService = Service()
WordPonderationService.AddHandler(ServerOperation.PONDERATION,ponderation_function)