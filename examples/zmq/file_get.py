#!/usr/bin/python2

import zmq 
import os
import sys

def get_file(path):
    '''
    '''
    dest = open(os.path.basename(path), 'w+')
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    socket.connect('tcp://127.0.0.1:4545')
    socket.setsocketopt(zmq.REQUEST, '')

    while True:
        data = socket.recv()
        if not data:
            break
        dest.write(data)
        if not socket.getsocketopt():
            break

if __name__ == '__main__':
    get_file(sys.argv[1])
