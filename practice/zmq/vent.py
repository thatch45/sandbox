#!/usr/bin/python
'''
Me figuring out the ventelator stuff in zeromq
'''
import sys
import zmq
import multiprocessing

PUSH = 'tcp://127.0.0.1:45555'
WORKERS = 10
MESSAGES = 10000000

def worker():
    '''
    A PULL worker
    '''
    context = zmq.Context()
    rec = context.socket(zmq.PULL)
    rec.connect(PUSH)

    while True:
        rec.recv()

def main():
    '''
    Run the foo!
    '''
    context = zmq.Context()
    push = context.socket(zmq.PUSH)
    push.bind(PUSH)
    for ind in range(WORKERS):
        multiprocessing.Process(target=worker).start()

    for ind in range(MESSAGES):
        push.send('foo')
    print 'Pushed messages'
    sys.exit(1)

if __name__ == '__main__':
    main()
