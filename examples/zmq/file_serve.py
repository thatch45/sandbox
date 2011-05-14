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
            sock.send('')
            continue
        fn = open(msg, 'rb')
        stream = True
        while stream:
            stream = fn.read(128)
            if stream:
                sock.send(stream, zmq.SNDMORE)
            else:
                sock.send(stream)

if __name__ == '__main__':
    server()
