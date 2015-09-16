__author__ = 'marczis'

import asyncore
import socket
import cPickle
import signal
import os

import webpage
from Config import Config

class SchedulerHandler(asyncore.dispatcher_with_send):
    def __init__(self, parent, arg):
        asyncore.dispatcher_with_send.__init__(self, arg)
        self.parent = parent
        self.data = ""

    def handle_read(self):
        self.data += self.recv(Config.getint("Networking", "receiver_buffer_size"))
        eom = self.data.find(";")
        if eom == -1:
            return

        msg = self.data[0:eom]
        self.data = self.data[eom+1:]

        x = cPickle.loads(msg)
        Config.getsites()[x.getId()].setResult(x)

    def handle_close(self):
        self.parent.unregisterClient(self.socket)
        asyncore.dispatcher_with_send.handle_close(self)


class Scheduler(asyncore.dispatcher):
    def __init__(self):
        asyncore.dispatcher.__init__(self)
        signal.signal(signal.SIGALRM, self.handleTimer)
        self.period = Config.getint("Scheduler", "period")
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((Config.get("Networking","listen_address"), Config.getint("Networking", "port")))
        self.listen(5) # TODO WHAT IS 5 ?
        self.wpc = [] # WebPageCheckers - so the workers registered to this scheduler
        self.wpciter = iter(self.wpc)
        self.remainingseconds = 0
        signal.alarm(self.period) #Starts the scheduler

    def enableScheduler(self):
        signal.alarm(self.remainingseconds)

    def disableScheduler(self):
        self.remainingseconds = signal.alarm(0)

    def unregisterClient(self, sock):
        print "Unregister: %s" % (sock)
        self.disableScheduler()
        self.wpc.remove(sock) #Should we have a lock here ?
        self.wpciter = iter(self.wpc) #Not optimal, but client registration, should not happen too often
        self.enableScheduler()

    def registerClient(self, sock):
        print "Register: %s" % (sock)
        self.disableScheduler()
        self.wpc.append(sock)
        self.wpciter = iter(self.wpc) #Same thoughts here.
        self.enableScheduler()
    
    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            # TODO use python logger here
            self.registerClient(sock)
            handler = SchedulerHandler(self, sock)

    def handleConnections(self):
        asyncore.loop() # TODO will this ever return ?

    def handleTimer(self, signum, frame):
        print "Scheduler tick"
        for i in Config.getsites():
            print i

        if not self.wpc:
            print "No workers connected. Skip iteration."
            signal.alarm(self.period)
            return

        for site in Config.getsites():
            if site.shouldSend(): #NOTE: You can call this once and ONLY ONCE, in every scheduler round
                try:
                    x = self.wpciter.next()
                except StopIteration:
                    self.wpciter = iter(self.wpc)
                    x = self.wpciter.next()

                site.sendMe(x)
                print "Sent %s to %s" % (site.getName(), x)
        signal.alarm(self.period)


