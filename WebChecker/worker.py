__author__ = 'marczis'

import socket
import cPickle
import time

class Worker:
    def __init__(self):
        self.scheduler = "localhost"
        self.port = 2424 # TODO put them into config
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.s.settimeout(1) #TODO Config

    def doWork(self):
        data = ""
        self.s.connect(("localhost", 2424)) # TODO Config
        while [ 1 ]:
            newdata = self.s.recv(8192) # TODO Change to bigger number
            if not newdata:
                self.s.close()
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                while [ 1 ]:
                    try:
                        print "Try to reconnect..." #TODO why not reconnect ?
                        self.s.connect(("localhost", 2424)) # TODO Config
                        break
                    except:
                        time.sleep(1) # TODO config
                continue

            data += newdata
            eom = newdata.find(";")
            if eom == -1:
                continue

            msg = data[0:eom]
            data = data[eom+1:]

            x = cPickle.loads(msg)
            x.doCheck()
            x.sendMe(self.s)
