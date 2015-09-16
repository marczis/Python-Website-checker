__author__ = 'marczis'

import cPickle
from Config import Config

class WebPage:
    OFFLINE = 0
    WRONG_ANSWER = 1
    ONLINE = 2

    def __init__(self, name="", url="", period=0, criteria=""):
        self.name = name
        self.url = url
        self.checkPeriod = period
        self.criteria = criteria
        self.status = WebPage.OFFLINE
        self.timetillcheck = period

    def doCheck(self):
        #TODO real check should be here
        print "Checked: %s" % self.url
        self.status = WebPage.ONLINE

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

    def __str__(self):
        return """%s
url:          %s
Check period: %s
Criteria    : %s
""" % (self.name, self.url, self.checkPeriod, self.criteria)

