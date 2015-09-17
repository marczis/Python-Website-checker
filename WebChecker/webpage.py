__author__ = 'marczis'

import cPickle
from Config import Config
import httplib2
import re
import socket
import time
import logging

class WebPage:
    OFFLINE = 0
    WRONG_ANSWER = 1
    ONLINE = 2

    def __init__(self, id, name="", url="", period=0, criteria=""):
        self.id = id
        self.name = name
        self.url = url
        self.checkPeriod = period
        self.criteria = re.compile(criteria, re.MULTILINE)
        self.timetillcheck = period
        self.status = WebPage.OFFLINE
        self.loadtime = 0 # in ms

    def doCheck(self):
        #TODO real check should be here
        logging.debug("Checking: %s" % self.name)
        try:
            con = httplib2.Http()
            start = time.time()
            resp, cont = con.request(self.url)
            self.loadtime = (time.time() - start) * 1000
        except httplib2.ServerNotFoundError:
            self.status = WebPage.OFFLINE
            logging.debug("OFFLINE by not found")
            return
        except socket.error:
            self.status = WebPage.OFFLINE
            logging.deubg("OFFLINE by socket error")
            return

        if resp["status"] == "200":
            self.status = WebPage.WRONG_ANSWER
            if self.criteria.search(cont) or not self.criteria:
                self.status = WebPage.ONLINE
        else:
            logging.debug("OFFLINE by status number: %s" % (resp["status"]))
            self.status = WebPage.OFFLINE


    def sendMe(self, sock):
        sock.send(cPickle.dumps(self) + ";")

    def shouldSend(self):
        self.timetillcheck-=Config.getint("Scheduler", "period")
        if self.timetillcheck <= 0:
            self.timetillcheck = self.checkPeriod
            return True
        return False

    def getName(self):
        return self.name

    def getId(self):
        return self.id

    def setResult(self, other):
        self.status = other.status
        self.loadtime = other.loadtime

    def __str__(self):
        return """%s ; url: %s ; Check period: %s ; Criteria: %s ; Status: %s ; LoadTime: %.3f ms""" \
               % (self.name, self.url, self.checkPeriod, self.criteria, self.status, self.loadtime)

