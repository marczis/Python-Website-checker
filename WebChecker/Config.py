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

            for id,name in  enumerate(pagesections):
                self.sites.append(webpage.WebPage(
                     id
                    ,name
                    ,self.config.get(name, "url")
                    ,self.config.getint(name, "check_period")
                    ,self.config.get(name, "criteria")
                ))

    def writeDeafults(self):
        self.config = ConfigParser.ConfigParser(allow_no_value=True)
        # self.config.add_section("General")

        self.config.add_section("Networking")
        self.config.set("Networking", "listen_address", "localhost")
        self.config.set("Networking", "#Server: bind to this address, use 0.0.0.0 for all interfaces")
        self.config.set("Networking", "#Client: scheduler's address")
        self.config.set("Networking", "port", "2424")
        self.config.set("Networking", "#Port to use, have to be same on Server / Client")
        self.config.set("Networking", "receiver_buffer_size", "8192")
        self.config.set("Networking", "#Buffer size of receiver socket, default should be okay.")
        self.config.set("Networking", "timeout", "30")
        self.config.set("Networking", "#Sockets' default timeout, default should be okay.")
        self.config.set("Networking", "reconnect_delay", 2) # TODO Change
        self.config.set("Networking", "#Seconds between retries on client side, when scheduler is gone.")

        self.config.add_section("Scheduler")
        self.config.set("Scheduler", "period", "2") #TODO Change to something
        self.config.set("Scheduler", "#Seconds between scheduler ticks, default should work well. Too low number may cause issues, but should be smaller than the smallest website checking period")

        name = "Test Site 1"
        self.config.add_section(name)
        self.config.set(name, "url", "http://www.mysite.domain/")
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

