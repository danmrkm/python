#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import time
import random

global PIDFILE
PIDFILE = './python_daemon.pid'


def main_proc():
    logfilepath = '/tmp/sample_daemon.log'

    while True:

        logfile = open(logfilepath, 'a')

        try:
            # Write time and random to logfile
            logfile.write(time.ctime() + " " +
                          str(random.randrange(10000000)) + "\n")

        finally:
            logfile.close()


def daemon_proc():

    pid = os.fork()

    # Child process
    if pid == 0:
        # Main process
        main_proc()

    # Parent process
    else:
        # Opening PIDFILE has failed
        if (os.path.exists(PIDFILE)):
            print('Error has occured. Check PIDFILE path.')
            sys.exit(1)
        # Opening PIDFILE has succeed.
        else:
            pidfile = open(PIDFILE, 'w')
            pidfile.write(str(pid)+"\n")
            pidfile.close()
            sys.exit()


if __name__ == '__main__':
    while True:
        daemon_proc()
