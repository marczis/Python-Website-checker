__author__ = 'marczis'

import asyncore
import socket
import logging
import re
from Config import Config

class WebServerHandler(asyncore.dispatcher_with_send):
    def __init__(self, arg):
        asyncore.dispatcher_with_send.__init__(self, arg)
        self.re = re.compile("GET / ")

    def handle_read(self):
        request = self.recv(Config.getint("Networking", "receiver_buffer_size"))
        if not self.re.search(request):
            return

        message = """
HTTP/1.1 200 Ok
Server: WebChecker
Connection: close

%s
""" % (Config.getWebContent())

        self.send(message)
        while ( len(self.out_buffer) > 0 ):
            self.initiate_send()
        self.close()

class WebServer(asyncore.dispatcher):
    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((Config.get("WebServer","listen_address"), Config.getint("WebServer", "port")))
        self.listen(5) # maximum number of queued connections
        logging.info("Started WebServer on %s:%s" % ((Config.get("WebServer","listen_address"), Config.getint("WebServer", "port"))))

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            handler = WebServerHandler(sock)
