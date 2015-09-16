#!/usr/bin/env python
__author__ = 'marczis'

import argparse
import sys

import WebChecker.scheduler
import WebChecker.worker

from WebChecker.Config import Config

if __name__ == "__main__":
    Config.getwebpages()
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-s", action="store_true", help="Starts the webchecker in server mode A.K.A. scheduler mode.")
    # pargs = parser.parse_args(sys.argv[1:])
    #
    # if (pargs.s):
    #     server = WebChecker.scheduler.Scheduler()
    #     server.handleConnections() #Async from here on
    # else:
    #     client = WebChecker.worker.Worker()
    #     client.doWork() # Endless loop #TODO ADD signal handling so can be stopped
