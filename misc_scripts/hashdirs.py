#!/usr/bin/python2

import hashlib
import sys
import random
import time
import pprint

def gen_hashes(n=10000000):
    ret = []
    start = time.time()
    for num in xrange(n):
        ret.append(hashlib.md5(str(random.randint(0, n))).hexdigest())
    print 'Genrated hash set in: {0} seconds'.format(time.time() - start)
    return ret

def form_dir(hashes):
    ret = {}
    for name in hashes:
        if not name[:2] in ret:
            ret[name[:2]] = [name[2:]]
        else:
            ret[name[:2]].append(name[2:])
    return ret

def find_high(dir_):
    high = 0
    for key, item in dir_.items():
        length = len(item)
        if length > high:
            high = length
    return high

def deviation(n):
    low = 999999999999999999999999999999
    high = 0
    for num in xrange(n):
        dir_num = dir_run(n)
        if dir_num < low:
            low = dir_num
        if dir_num > high:
            high = dir_num
    return {'high': high, 'low': low}


def dir_run(n):
    '''
    '''
    hashes = gen_hashes(n)
    dir_ = form_dir(hashes)
    high = find_high(dir_)
    print high
    return high

if __name__ == '__main__':
    if sys.argv[2].startswith('d'):
        pprint.pprint(deviation(int(sys.argv[1])))
    else:
        dir_run(int(sys.argv[1]))
