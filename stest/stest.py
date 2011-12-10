import time
import cPickle as pickle
import random
import json
import pprint
import os
import sys

import msgpack
import yaml


class STest(object):
    '''
    Manage serialization tests
    '''
    def __init__(self, opts):
        self.opts = opts
        self.bdata = self.big_data()
        self.cdata = self.complex_data()

    def complex_data(self, seed=100):
        '''
        Generate a complex dict with all basic types
        '''
        print 'generating complex data'
        data = {}
        for ind in range(seed):
            data[ind] = 'cheese is good and tasty'
            data[ind + seed] = {ind: ['bannana', 'orange']}
            data[ind + seed + seed] = []
            for ind_ in range(seed):
                data[ind + seed + seed].append(ind_)
        return data

    def big_data(self):
        '''
        Return a dict with binary strings of varying length
        '''
        print 'generating big data'
        data = {}
        for subdir in ['/bin', '/sbin']:
            for fn_ in os.listdir(subdir):
                full = os.path.join(subdir, fn_)
                if os.path.isfile(full):
                    try:
                        data[full] = open(full, 'r').read()
                    except:
                        pass
        return data

    def msg_pack(self):
        '''
        Time message pack for the given data types
        '''
        comp_time = time.time()
        msg_cdata = msgpack.packb(self.cdata)
        print 'Complex data packed in {0} seconds'.format(time.time() - comp_time)
        open('/tmp/msg_complex_data', 'w+').write(msg_cdata)
        big_time = time.time()
        msg_bdata = msgpack.packb(self.bdata)
        print 'Big data packed in {0} seconds'.format(time.time() - big_time)
        open('/tmp/msg_big_data', 'w+').write(msg_bdata)
        comp_time = time.time()
        msg_cdata_post = msgpack.loads(msg_cdata)
        print 'Complex data unpacked in {0} seconds'.format(time.time() - comp_time)
        big_time = time.time()
        msg_bdata_post = msgpack.loads(msg_bdata)
        print 'Big data unpacked in {0} seconds'.format(time.time() - big_time)

    def pickle_pack(self):
        '''
        Run the test with cpickle
        '''
        comp_time = time.time()
        p_cdata = pickle.dumps(self.cdata)
        print 'Complex data pickled in {0} seconds'.format(time.time() - comp_time)
        open('/tmp/p_complex_data', 'w+').write(p_cdata)
        big_time = time.time()
        p_bdata = pickle.dumps(self.bdata)
        print 'Big data pickled in {0} seconds'.format(time.time() - big_time)
        open('/tmp/p_big_data', 'w+').write(p_bdata)
        comp_time = time.time()
        p_cdata_post = pickle.loads(p_cdata)
        print 'Complex data unpickled in {0} seconds'.format(time.time() - comp_time)
        big_time = time.time()
        p_bdata_post = pickle.loads(p_bdata)
        print 'Big data unpickled in {0} seconds'.format(time.time() - big_time)


    def json_pack(self):
        '''
        Does not work
        Run the test with JSON
        '''
        comp_time = time.time()
        j_cdata = json.dumps(self.cdata)
        print 'Complex data JSON\'d in {0} seconds'.format(time.time() - comp_time)
        open('/tmp/json_complex_data', 'w+').write(j_cdata)
        big_time = time.time()
        j_bdata = json.dumps(self.bdata)
        print 'Big data JSON\'d in {0} seconds'.format(time.time() - big_time)
        open('/tmp/json_big_data', 'w+').write(j_bdata)
        comp_time = time.time()
        j_cdata_post = json.loads(j_cdata)
        print 'Complex data unJSON\'d in {0} seconds'.format(time.time() - comp_time)
        big_time = time.time()
        j_bdata_post = json.loads(j_bdata)
        print 'Big data unJSON\'d in {0} seconds'.format(time.time() - big_time)

    def yaml_pack(self):
        '''
        Run the test with YAML
        '''
        comp_time = time.time()
        y_cdata = yaml.dump(self.cdata)
        print 'Complex data YAML\'d in {0} seconds'.format(time.time() - comp_time)
        open('/tmp/yaml_complex_data', 'w+').write(y_cdata)
        big_time = time.time()
        y_bdata = yaml.dump(self.bdata)
        print 'Big data YAML\'d in {0} seconds'.format(time.time() - big_time)
        open('/tmp/yaml_big_data', 'w+').write(y_bdata)
        comp_time = time.time()
        y_cdata_post = yaml.load(y_cdata)
        print 'Complex data unYAML\'d in {0} seconds'.format(time.time() - comp_time)
        big_time = time.time()
        y_bdata_post = yaml.load(y_bdata)
        print 'Big data unYAML\'d in {0} seconds'.format(time.time() - big_time)

if __name__ == '__main__':
    serial = STest({})
    serial.msg_pack()
    serial.pickle_pack()
    #serial.json_pack()
    serial.yaml_pack()
