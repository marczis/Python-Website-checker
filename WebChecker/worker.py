__author__ = 'marczis'

import socket
import cPickle
import time

from Config import Config

class Worker:
    def __init__(self):
        self.scheduler = (Config.get("Networking", "listen_address"), Config.getint("Networking", "port"))
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(Config.getint("Networking", "timeout"))

    def connect(self):
        while [ 1 ]:
            try:
                print "Try to reconnect..."
                self.s.connect(self.scheduler)
                return
            except:
                time.sleep(Config.getint("Networking", "reconnect_delay"))

    def doWork(self):
        data = ""
        self.connect()

        while [ 1 ]:
            try:
                newdata = self.s.recv(8192) # TODO Change to bigger number
            except socket.timeout as e:
                continue

            if not newdata:
                self.s.close()
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connect()

            data += newdata
            eom = newdata.find(";")
            if eom == -1:
                continue

            msg = data[0:eom]
            data = data[eom+1:]

            x = cPickle.loads(msg)
            x.doCheck()
            x.sendMe(self.s)
