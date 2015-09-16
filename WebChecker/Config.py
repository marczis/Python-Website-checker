__author__ = 'marczis'

import ConfigParser
import os.path
import webpage

CONFIGFILE="./config"

class Config:
    Config = None

    class MissingConfig:
        pass

    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.sites = []
        #Check if config file exists
        if not os.path.isfile(CONFIGFILE):
            self.writeDeafults()
        else:
            self.config.read(CONFIGFILE)
            pagesections = self.config.sections()
            pagesections.remove("General")
            pagesections.remove("Networking")
            pagesections.remove("Scheduler")

            for name in  pagesections:
                self.sites.append(webpage.WebPage(
                     name
                    ,self.config.get(name, "url")
                    ,self.config.getint(name, "check_period")
                    ,self.config.get(name, "criteria")
                ))

    def writeDeafults(self):
        self.config.add_section("General")

        self.config.add_section("Networking")
        self.config.set("Networking", "listen_address", "localhost")
        self.config.set("Networking", "port", "2424")
        self.config.set("Networking", "receiver_buffer_size", "8192")
        self.config.set("Networking", "timeout", "30")
        self.config.set("Networking", "reconnect_delay", 2) # TODO Change

        self.config.add_section("Scheduler")
        self.config.set("Scheduler", "period", "2") #TODO Change to something

        name = "Test Site 1"
        self.config.add_section(name)
        self.config.set(name, "url", "www.mysite.domain")
        self.config.set(name, "check_period", "30")
        self.config.set(name, "criteria", "Pong")
        with open(CONFIGFILE, "w+") as x:
            self.config.write(x)

        raise Config.MissingConfig

    @staticmethod
    def createInstance():
        if not Config.Config:
            Config.Config = Config()

    @staticmethod
    def get(section, key):
        Config.createInstance()
        return Config.Config.config.get(section, key)

    @staticmethod
    def getint(section, key):
        Config.createInstance()
        return Config.Config.config.getint(section, key)

    @staticmethod
    def getsites():
        Config.createInstance()
        return Config.Config.sites

