__author__ = 'marczis'

import cPickle
from Config import Config

class WebPage:
    OFFLINE = 0
    WRONG_ANSWER = 1
    ONLINE = 2

    def __init__(self, id, name="", url="", period=0, criteria=""):
        self.id = id
        self.name = name
        self.url = url
        self.checkPeriod = period
        self.criteria = criteria
        self.timetillcheck = period
        self.status = WebPage.OFFLINE
        self.loadtime = 0

    def doCheck(self):
        #TODO real check should be here
        print "Checked: %s" % self.name
        self.status = WebPage.ONLINE
        self.loadtime = self.id

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
        return """%s
url:          %s
Check period: %s
Criteria    : %s
Status      : %s
LoadTime    : %s
""" % (self.name, self.url, self.checkPeriod, self.criteria, self.status, self.loadtime)

