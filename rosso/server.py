import zmq
import time
import pickle

def serve():
    '''
    '''
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:5555')

    while True:
        message = socket.recv()
        print pickle.loads(message)['foo']
        socket.send("world")

if __name__ == '__main__':
    serve()
