'''
writing subrutine

subrutine for write the strings in the file
'''

from sys import argv,exit
from multiprocessing import freeze_support,Value,Process,Lock,cpu_count
from core import StringGenerator,removefile

def write_strings(total:int,path:str,lock,min_length:int,max_length:int,pattern:str):
    generator = StringGenerator(
        pattern=pattern,
        min_length=min_length,
        max_length=max_length
    )
    text = ''
    for word in generator.GenerateStrings(total):
        text += f'{word}\n'
        pass
    with lock:
        with open(path,'a') as writer:
            writer.write(text)
            pass
        pass
    pass


if __name__ == '__main__':

    _,path,pattern,min_chars,max_chars,count,cpu = argv
    cpus = cpu_count()
    lock = Lock()
    freeze_support()

    with open(f'{path}.lock','w') as f:
        pass

    processes_needed = int(count) // 10000
    if (int(count) // 10000)*10000 < int(count):
        processes_needed += 1
        pass
    total = int(count)

    while processes_needed > 0:
        processes = []    
        for i in range(min(cpus*int(cpu),processes_needed)):
            p_total = 10000 if total > 10000 else total
            p = Process(target=write_strings,args=(p_total,path,lock,int(min_chars),int(max_chars),pattern),name=f'p{i}',daemon=True)
            total -= p_total
            processes_needed -= 1
            p.start()
            processes.append(p)
            pass
        for p in processes:
            p.join()
            pass
        pass

    removefile(f'{path}.lock')