__author__ = 'marczis'

import asyncore
import socket
import cPickle

import webpage

class SchedulerHandler(asyncore.dispatcher_with_send):
    def __init__(self, arg):
        asyncore.dispatcher_with_send.__init__(self, arg)
        self.data = ""
        #TODO Push first task from here.
        # REMOVE: Only for testing
        x = webpage.WebPage()
        self.send(cPickle.dumps(x) + ";")

    def handle_read(self):
        self.data += self.recv(8192) # TODO make it config parameter
        eom = self.data.find(";")
        if eom == -1:
            return

        msg = self.data[0:eom]
        self.data = self.data[eom+1:]

        x = cPickle.loads(msg)
        print x.status


class Scheduler(asyncore.dispatcher):
    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(("localhost", 2424)) # TODO CONFIG PARAMETER
        self.listen(5) # TODO WHAT IS 5 ?
        self.wpc = [] # WebPageCheckers - so the workers registered to this scheduler

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            # TODO use python logger here
            print "Incommminnngggg.... %s:%s" % (sock,addr)
            handler = SchedulerHandler(sock)

    def handleConnections(self):
        asyncore.loop() # TODO will this ever return ?