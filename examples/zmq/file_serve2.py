#!/usr/bin/python2

import zmq
import os

def server():
    '''
    Setup a VERY simple file server
    '''
    # Set up the zeromq context and REP socket
    context = zmq.Context(1)
    sock = context.socket(zmq.REP)
    sock.bind('tcp://*:4545')

    BUFF = 64

    # Start the server loop
    while True:
        # Set up a return container
        ret = {}
        # Recieve the location of the file to serve
        msg = sock.recv_pyobj()
        # Verify that the file is available
        if not os.path.isfile(msg['path']):
            sock.send('')
            continue
        # Open the file for reading
        fn = open(msg['path'], 'rb')
        fn.seek(msg['loc'])
        ret['body'] = fn.read(BUFF)
        ret['loc'] = fn.tell()
        sock.send_pyobj(ret)

if __name__ == '__main__':
    server()
