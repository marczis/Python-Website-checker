__author__ = 'marczis'

import asyncore
import socket
import cPickle
import signal
import logging
import asynchat

from Config import Config

class SchedulerHandler(asynchat.async_chat):
    def __init__(self, parent, arg):
        asynchat.async_chat.__init__(self, sock=arg)
        self.parent = parent
        self.data = []
        self.set_terminator("#EOM#")

    def collect_incoming_data(self, data):
        self.data.append(data)

    def found_terminator(self):
        x = cPickle.loads("".join(self.data))
        Config.getsites()[x.getId()].setResult(x)
        self.data = []
        logging.info("%s: URL: %s Status: %s Loadtime: %.0f ms" % (x.getName(), x.getURL(), x.getStatus(), x.getLoadTime()))

    def handle_close(self):
        self.parent.unregisterClient(self)
        asynchat.async_chat.handle_close(self)


class Scheduler(asyncore.dispatcher):
    def __init__(self):
        asyncore.dispatcher.__init__(self)
        signal.signal(signal.SIGALRM, self.handleTimer)
        self.period = Config.getint("Scheduler", "period")
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((Config.get("Networking","listen_address"), Config.getint("Networking", "port")))
        self.listen(5) # maximum number of queued connections
        self.wpc = [] # WebPageCheckers - so the workers registered to this scheduler
        self.wpciter = iter(self.wpc)
        self.remainingseconds = 0
        self.logonce = True
        signal.alarm(self.period) #Starts the scheduler

    def enableScheduler(self):
        signal.alarm(self.remainingseconds)

    def disableScheduler(self):
        self.remainingseconds = signal.alarm(0)

    def unregisterClient(self, chat):
        logging.info("Unregister worker: %s" % (chat))
        self.disableScheduler()
        self.wpc.remove(chat) #Should we have a lock here ?
        self.wpciter = iter(self.wpc) #Not optimal, but client registration, should not happen too often
        self.enableScheduler()

    def registerClient(self, chat):
        logging.info("Register worker: %s" % (chat))
        self.disableScheduler()
        self.wpc.append(chat)
        self.wpciter = iter(self.wpc) #Same thoughts here.
        self.enableScheduler()
    
    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            # TODO use python logger here
            handler = SchedulerHandler(self, sock)
            self.registerClient(handler)

    def handleTimer(self, signum, frame):
        logging.debug("Scheduler tick")
        for i in Config.getsites():
            logging.debug(i)

        if not self.wpc:
            if self.logonce:
                logging.info("No workers connected.")
                self.logonce = False
            signal.alarm(self.period)
            return
        self.logonce = True

        for site in Config.getsites():
            if site.shouldSend(): #NOTE: You can call this once and ONLY ONCE, in every scheduler round
                try:
                    x = self.wpciter.next()
                except StopIteration:
                    self.wpciter = iter(self.wpc)
                    x = self.wpciter.next()

                site.sendMe(x)
                logging.debug("Sent \"%s\" to %s:%s" % (site.getName(), x.getpeername()[0], x.getpeername()[1]))
        signal.alarm(self.period)


