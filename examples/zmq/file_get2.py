#!/usr/bin/python2

import zmq 
import os
import sys

def get_file(path):
    '''
    A VERY simple client to get files from the zeromq VERY simple file server
    '''
    # Open up the file we are going to write to
    dest = open(os.path.basename(path), 'w+')
    # Set up the zeromq context and socket
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    socket.connect('tcp://127.0.0.1:4545')

    msg = {'loc': 0,
           'path': path}

    while True:
        # send the desired file and the location to the server
        socket.send_pyobj(msg)
        # Start grabing data
        data = socket.recv_pyobj()
        # Write the chunk to the file
        if data['body']:
            dest.write(data['body'])
            msg['loc'] = dest.tell()
        else:
            break

if __name__ == '__main__':
    get_file(sys.argv[1])
