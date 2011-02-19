import zmq
import pickle

context = zmq.Context()
socket = context.socket(zmq.REQ)

print 'connecting to the server'
socket.connect('tcp://localhost:5555')

s = {'foo': 'bar',
     'baz': 6}

socket.send(pickle.dumps(s, -1))
print 'got back ' + socket.recv()
