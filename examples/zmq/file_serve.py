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

    # Start the server loop
    while True:
        # Recieve the location of the file to serve
        msg = sock.recv()
        # Verify that the file is available
        if not os.path.isfile(msg):
            sock.send('')
            continue
        # Open the file for reading
        fn = open(msg, 'rb')
        stream = True
        # Start reading in the file
        while stream:
            # Read the file bit by bit
            stream = fn.read(128)
            if stream:
                # If the stream has more to send then send more
                sock.send(stream, zmq.SNDMORE)
            else:
                # Finish it off
                sock.send(stream)

if __name__ == '__main__':
    server()
