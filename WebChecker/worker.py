__author__ = 'marczis'

import socket
import cPickle
import time
import logging
import asynchat

from Config import Config
class Worker(asynchat.async_chat):
    def __init__(self):
        asynchat.async_chat.__init__(self)
        self.data = []
        self.logonce = False
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.scheduler = (Config.get("Networking", "listen_address"), Config.getint("Networking", "port"))
        self.doConnect()
        self.set_terminator("#EOM#")

    def doConnect(self):
        while [ 1 ]:
            try:
                if self.logonce:
                    logging.info("Try to reconnect: %s:%s" % self.scheduler)
                    self.logonce = False
                self.connect(self.scheduler)
                self.logonce = True
                logging.info("Connected.")
                return
            except:
                time.sleep(Config.getint("Networking", "reconnect_delay"))

    def collect_incoming_data(self, data):
        self.data.append(data)

    def found_terminator(self):
        x = cPickle.loads("".join(self.data))
        self.data = []
        x.doCheck()
        x.sendMe(self)