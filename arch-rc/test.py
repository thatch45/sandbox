import time
import signal

def handle15(signum, frame):
    '''
    handle a sigterm
    '''
    print('Some fool tried to SIGTERM me!')

signal.signal(signal.SIGTERM, handle15)

while True:
    pass
