__author__ = 'marczis'

import cPickle

class WebPage:
    OFFLINE = 0
    ONLINE = 1

    def __init__(self):
        self.url = ""
        self.timeout = 0
        self.checkPeriod = 0
        self.status = WebPage.OFFLINE
        self.name = ""
        self.filename = ""

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def doCheck(self):
        print "Checked: %s" % self.url
        self.status = WebPage.ONLINE

    def sendMe(self, sock):
        sock.send(cPickle.dumps(self) + ";")

    def __str__(self):
        return """%s
url: %s
""" % (self.name, self.url)

#Some notes: cPickle.dump(obj, file); cPickle.load(file)
#