#!/usr/bin/env python
__author__ = 'marczis'

import argparse
import sys
import logging
import socket

import WebChecker.scheduler
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
            server = WebChecker.scheduler.Scheduler()
            server.handleConnections() #Async from here on
        else:
            logging.info("Webchecker started as Worker")
            client = WebChecker.worker.Worker()
            client.doWork() # Endless loop #TODO ADD signal handling so can be stopped

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

if __name__ == "__main__":
    main()