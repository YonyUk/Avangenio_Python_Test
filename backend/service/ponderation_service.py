'''
ponderation service

service for the word's ponderations
'''
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from .service import Service
from protocol import ServerOperation,Request,Status
import re
import logging
import datetime
from multiprocessing import Process,Lock,Array,cpu_count

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s [%(threadName)s] %(levelname)s: %(message)s')

class WordPonderationService(Service):

    _start_operation_time = None
    _log = ''
    _words = []
    _special_pattern = 'aa|AA|aA|Aa'
    _results = None
    _lock = Lock()

    def __init__(self):
        super().__init__()
        super().AddHandler(ServerOperation.PONDERATION,lambda request:self._ponderation_function(request))
        super().AddHandler(ServerOperation.START_FILE_PONDERATION,lambda request:self._start_ponderation())
        super().AddHandler(ServerOperation.END_FILE_PONDERATION,lambda request:self._end_ponderation())
        super().AddHandler(ServerOperation.SEND_FILE,lambda request:self._recv_file(request))
        pass

    def _start_ponderation(self):
        
        self._start_operation_time = datetime.datetime.now()
        return {
            'Status':Status.OK,
            'StatusMessage':'OK',
        }

    def _end_ponderation(self):
        t = datetime.datetime.now() - self._start_operation_time
        self._start_operation_time = None
        logging.info(f'Processed in {t}')
        return {
            'Status':Status.OK,
            'StatusMessage':'OK',
            'Body':{
                'time':str(t)
            }
        }

    def _recv_file(self,request:Request):
        self._words = request.Body['words']
        self._results = Array('d',len(self._words))
        return {
            'Status':Status.OK,
            'StatusMessage':'OK'
        }
    
    def _ponderate_words(self,words:list):
        for word in words:
            self._results[word] = get_word_ponderation(self._words[word],self._special_pattern)
            pass
        pass

    def _ponderation_function(self,request:Request):
        process_by_cpu = request.Body['process_by_cpu']
        strings_by_process = request.Body['strings_by_process']
        total = len(self._words)
        if total < strings_by_process:
            strings_by_process = total // (cpu_count()*process_by_cpu)
            pass
        process_needed = total // strings_by_process
        if process_needed*strings_by_process < total:
            process_needed += 1
            pass
        if __name__ == '__mp_main__':
            return
        start = 0
        while process_needed > 0:
            processes = []
            for i in range(min(cpu_count()*process_by_cpu,process_needed)):
                p = Process(target=lambda:self._ponderate_words([i for i in range(start,start + strings_by_process)]),name=f'p{i}')
                processes.append(p)
                p.start()
                start += strings_by_process
                pass
            for process in processes:
                process.join()
                pass
            process_needed -= cpu_count()*process_by_cpu
            pass
        result = [f'{self._words[i]}: {self._results[i]}' for i in range(len(self._words))]
        self._words = None
        self._results = None
        logging.info(self._log)
        self._log = ''
        return {
            'Status':Status.OK,
            'StatusMessage':'OK',
            'Body':{
                'results':result
            }
        }

    pass

def get_word_ponderation(string:str,special_pattern:str):
    # pattern of the text
    total_pattern = '\S'
    digits_pattern = '\d'
    whitespace_pattern = '\s'

    if re.search(special_pattern,string) != None:
        logging.info(f"\nPattern \"{special_pattern}\" rule detected >>> {string}\n")
        return 1000
    digits_count = len(re.findall(digits_pattern,string))
    whitespace_count = len(re.findall(whitespace_pattern,string))
    chars_count = len(re.findall(total_pattern,string)) - digits_count
    result = (chars_count * 1.5 + digits_count * 2)/whitespace_count
    return result