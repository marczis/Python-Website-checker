__author__ = 'marczis'

import asyncore
import socket
import cPickle
import signal
import os

import webpage

class SchedulerHandler(asyncore.dispatcher_with_send):
    def __init__(self, parent, arg):
        asyncore.dispatcher_with_send.__init__(self, arg)
        self.parent = parent
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
        print "%s: %s" % (x.url, x.status)

    def handle_close(self):
        self.parent.unregisterClient(self.socket)
        asyncore.dispatcher_with_send.handle_close(self)


class Scheduler(asyncore.dispatcher):
    def __init__(self):
        asyncore.dispatcher.__init__(self)
        signal.signal(signal.SIGALRM, self.handleTimer)
        self.period = 5 #TODO config
        signal.alarm(self.period)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(("localhost", 2424)) # TODO CONFIG PARAMETER
        self.listen(5) # TODO WHAT IS 5 ?
        self.wpc = [] # WebPageCheckers - so the workers registered to this scheduler

    def unregisterClient(self, sock):
        print "Unregister: %s" % (sock)
        self.wpc.remove(sock) #TODO should we have a lock here ?

    def registerClient(self, sock):
        print "Register: %s" % (sock)
        self.wpc.append(sock)
    
    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            # TODO use python logger here
            print "Incommminnngggg.... %s:%s" % (sock,addr)
            self.registerClient(sock)
            handler = SchedulerHandler(self, sock)

    def handleConnections(self):
        asyncore.loop() # TODO will this ever return ?

    def handleTimer(self, signum, frame):
        print "Time to schedule."
        #TODO remove just for testing
        x = webpage.WebPage()
        for z in self.wpc:
            x.url="%s" % z
            z.send(cPickle.dumps(x) + ";")
            print "sent for: %s" % (z)
        signal.alarm(self.period)
