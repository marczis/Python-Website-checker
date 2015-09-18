#!/usr/bin/env python
__author__ = 'marczis'

import argparse
import sys
import logging
import socket
import ConfigParser
import asyncore

import WebChecker.scheduler
import WebChecker.webserver
import WebChecker.worker
from WebChecker.Config import Config

def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-s", action="store_true", help="Starts the webchecker in server mode A.K.A. scheduler mode.")
        parser.add_argument("-d", action="store_true", help="Enable debug logs")
        parser.add_argument("-c", action="store_true", help="Show logs on console too")
        pargs = parser.parse_args(sys.argv[1:])

        loglevel = logging.INFO
        if pargs.d:
            loglevel = logging.DEBUG

        logfile = "webchecker-worker.%s.log" % (socket.gethostname())
        if pargs.s:
            logfile = "webchecker-scheduler.%s.log" % (socket.gethostname())

        logging.basicConfig(filename=logfile, level=loglevel)

        if pargs.c:
            console = logging.StreamHandler()
            console.setLevel(loglevel)
            console.setFormatter(logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s'))
            logging.getLogger('').addHandler(console)

        if pargs.s:
            logging.info("Webchecker started as Scheduler")
            scheduler = WebChecker.scheduler.Scheduler()
            webserver = WebChecker.webserver.WebServer()
        else:
            logging.info("Webchecker started as Worker")
            client = WebChecker.worker.Worker()

        asyncore.loop()

    except Config.MissingConfig:
        logging.error("Started without config.")
        print """
You started the webchecker without proper configuration, a default config file is created for you.
Please check and modify it according to your needs.
"""

    except socket.error as e:
        logging.error("Network problem: %s" % (e))
        print """
Network problem. If you started the application in server mode, please check the port & address options,
plus if you have access rights on the system to open that port.
If you started in client mode, please double check the server address and check if you have any
blocking firewall or other entity in the way.

Low level error message:
%s
""" % (e)

    except ConfigParser.NoOptionError as e:
        logging.error("Config error: %s" % (e))
        print """
Ooops. Looks like you have a problem in your config file. Please check it again. In worst case delete it, so I can
regenerate a working one for you with default values.

Low level error message:
%s
""" % (e)

if __name__ == "__main__":
    main()