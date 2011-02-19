'''
The rpc client
'''

import os
import zmq
import cPickle as pickle

class ReqClient(object):
    '''
    Cretaes a request rpc client, this client is used to make direct calls
    to REP server
    '''
    def __init__(self):
        '''
        the client, duh
        '''
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)

    def connect(self, remote):
        '''
        makes a socket
        '''
        self.socket.connect(remote)

    def command(self, func, args=()):
        '''
        Invoke the following command on the remote system, func is a string,
        args is a tuple.
        '''
        data = {'name': func,
                'args': args}
        socket.send(pickle.dumps(data))
        return pickle.loads(socket.recv())

class SubClient(object):
    '''
    Creates a client which connects to a publish server and awaits publish
    commands.
    '''
    def __init__(self, name, master, funcs=[]):
        '''
        Can be initialized with a list of function objects which can be called
        by the publisher
        '''
        self.name = name
        self.master = master
        self.funcs = self.__populate_funcs(funcs)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)

    def __populate_funcs(self, funcs):
        '''
        Taks a list of function objects and return a dict with named keys
        '''
        ret = {}
        for func in self.funcs:
            ret[func.__name__] = func
        return ret

    def add_funcs(self, funcs):
        '''
        Takes a list of function objects and adds them to the functions
        '''
        for func in funcs:
            self.funcs[func._name_] = func

    def add_func(self, func):
        '''
        Add a fingle function object to the system
        '''
        self.funcs[func.__name__] = func

    def _send_result(self, ret):
        '''
        Returns the result of the function to the specified server in the cmd 
        structure
        '''
        client = ReqClient()
        client.connect(remote)
        client.command('return')

    def connect(self):
        '''
        Connect to the specified publish server
        '''
        self.socket.connect(remote)
        while True:
            cmd = piclke.loads(socket.recv())
            ret = ''
            try:
                ret = apply(self.funcs[cmd['name']]['func'],
                    cmd['args'])
            except:
                ret =  'No such function'
            self._send_result(cmd['remote'], ret)
