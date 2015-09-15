__author__ = 'marczis'

import socket
import cPickle

class Worker:
    def __init__(self):
        self.scheduler = "localhost"
        self.port = 2424 # TODO put them into config
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("localhost", 2424)) # TODO Config

    def doWork(self):
        data = ""
        while [ 1 ]:
            data += self.s.recv(1) # TODO Change to bigger number
            eom = data.find(";")
            if eom == -1:
                continue

            msg = data[0:eom]
            data = data[eom+1:]

            x = cPickle.loads(msg)
            x.doCheck()
            self.s.send(cPickle.dumps(x) + ";")

            #TODO if socket dies