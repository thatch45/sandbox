import random
import time

def get_data():
    data = set()
    for n in xrange(10000):
        data.add(random.randrange(1, 999999999999999))
    return data, list(data)

def run():
    sdata, ldata = get_data()

    sstart = time.time()
    for comp in ldata:
        if comp in sdata:
            pass
    stime = time.time() - sstart
    lstart = time.time()
    for comp in ldata:
        if comp in ldata:
            pass
    ltime = time.time() - lstart

    print 'Set time: {0}'.format(stime)
    print 'List time: {0}'.format(ltime)

run()
