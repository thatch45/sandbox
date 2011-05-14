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

    while True:
        data = socket.recv_multipart()
        if not data:
            break
        dest.write(data)

if __name__ == '__main__':
    get_file(sys.argv[1])
