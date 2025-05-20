from multiprocessing import Process,freeze_support,Lock,Value
import time

def Count(t,l:Lock,value:Value,increment:int):
    for _ in range(t):
        with l:
            value.value += increment


if __name__ == '__main__':
    count = Value('i',0)
    lock = Lock()
    freeze_support()
    val = 50000
    p1 = Process(name='my_process',target=Count,args=(val,lock,count,1),daemon=True)
    p2 = Process(name='my_process_2',target=Count,args=(val,lock,count,-1),daemon=True)
    p1.start()
    p2.start()

    while(p1.is_alive() or p2.is_alive()):
        print(count.value)
        time.sleep(1)
    
    print('final value:',count.value)
    print('synchronized:',count.value==0)

    p1.terminate()
    p1.close()
    p2.terminate()
    p2.close()
