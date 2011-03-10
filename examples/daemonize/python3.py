#!/usr/bin/python3
'''
Daemonize a process in python3
'''

import os
import sys

def daemonize():
    '''
    Daemonize a process
    '''
    try: 
        pid = os.fork() 
        if pid > 0:
            # exit first parent
            sys.exit(0) 
    except OSError as e:
        print("fork #1 failed: %d (%s)" % (e.errno, e.strerror), file=sys.stderr)
        sys.exit(1)

    # decouple from parent environment
    os.chdir("/") 
    os.setsid() 
    os.umask(0o22)

    # do second fork
    try: 
        pid = os.fork() 
        if pid > 0:
            # print "Daemon PID %d" % pid 
            sys.exit(0) 
    except OSError as e:
        print("fork #2 failed: %d (%s)" % (e.errno, e.strerror), file=sys.stderr)
        sys.exit(1) 

    dev_null = open('/dev/null','w') 
    os.dup2(dev_null.fileno(), sys.stdin.fileno()) 
    os.dup2(dev_null.fileno(), sys.stdout.fileno()) 
    os.dup2(dev_null.fileno(), sys.stderr.fileno()) 

