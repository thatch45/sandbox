#!/usr/bin/python2

import zmq

def server():
    '''
    Setup a VERY simple file server
    '''
    context = zmq.Context(1)
    sock = context.socket(zmq.REP)
    sock.bind('tcp://*:4545')

    while True:
        msg = sock.recv()
        if not os.path.isfile(msg):
            sock.send('File Not Found')
            continue
        fn = open(msg, 'rb')
        stream = fn.read(128)
        if not stream:
            sock.send(stream)
        while stream:
            sock.send_multipart(stream)

if __name__ == '__main__':
    server()
