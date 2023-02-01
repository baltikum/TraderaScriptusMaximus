from multiprocessing import Process,Queue,Pipe
from test import BIDDERPROCESS
from test3 import WSGIPROCESS
import time





if __name__ == '__main__':


    QUE_FROM_BIDDER = Queue()
    QUE_TO_BIDDER = Queue()
    QUE_FROM_WSGI = Queue()
    QUE_TO_WSGI = Queue()


    bidderProcess = Process(target=BIDDERPROCESS, args=(QUE_FROM_BIDDER,QUE_TO_BIDDER))
    bidderProcess.daemon = True
    bidderProcess.start()
    wsgiProcess = Process(target=WSGIPROCESS, args=(QUE_FROM_WSGI,QUE_TO_WSGI))
    wsgiProcess.daemon = True
    wsgiProcess.start()


    #WAIT FOR BIDDER BOOT
    while True:
        if not QUE_FROM_BIDDER.empty():
            msg = QUE_FROM_BIDDER.get()
            print(msg)
            if msg['STATUS'] == "READY":
                break
            exit(-1)
        time.sleep(5)

    #WAIT FOR WSGI BOOT
    while True:
        if not QUE_FROM_WSGI.empty():
            msg = QUE_FROM_WSGI.get()
            if msg['STATUS'] == "READY":
                break
            exit(-1)
        time.sleep(5)
    
    while True:
        if not QUE_FROM_WSGI.empty():
            msg = QUE_FROM_WSGI.get()
            print(msg)
        time.sleep(2)
