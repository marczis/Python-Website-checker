__author__ = 'marczis'


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

    def doCheck(self):
        print "Checked: %s" % self.url
        self.status = WebPage.ONLINE

#Some notes: cPickle.dump(obj, file); cPickle.load(file)
#