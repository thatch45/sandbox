#!/usr/bin/env python2

import subprocess

def ping(n=100):
    '''
    Run test.ping n times, default to 100
    '''
    cmd = 'salt "*" test.ping'
    for ind in range(n):
        subprocess.Popen(cmd, shell=True)
        

if __name__ == '__main__':
    ping()
