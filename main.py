#!/usr/bin/env python
__author__ = 'marczis'

import argparse
import sys
import socket

import WebChecker.scheduler
import WebChecker.worker
from WebChecker.Config import Config

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-s", action="store_true", help="Starts the webchecker in server mode A.K.A. scheduler mode.")
        pargs = parser.parse_args(sys.argv[1:])

        if (pargs.s):
            server = WebChecker.scheduler.Scheduler()
            server.handleConnections() #Async from here on
        else:
            client = WebChecker.worker.Worker()
            client.doWork() # Endless loop #TODO ADD signal handling so can be stopped
    except Config.MissingConfig:
        print """
You started the webchecker without proper configuration, a default config file is created for you.
Please check and modify it according to your needs.
"""

#     except socket.error as e:
#         print """
# Network problem. If you started the application in server mode, please check the port & address options,
# plus if you have access rights on the system to open that port.
# If you started in client mode, please double check the server address and check if you have any
# blocking firewall or other entity in the way.
#
# Low level error message:
# %s
# """ % (e)