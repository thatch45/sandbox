'''
Wrap the stuff pycrypto needs for reading rsa keys
'''

# Import python docs
import sys
import base64
import binascii

# Import PyCrypto
from Crypto.PublicKey import RSA

def prep_base(path):
    '''
    Prep the base64 data from a key
    '''
    # This should manage more types of pem formatted keys
    lines = open(path, 'r').readlines()
    return base64.decodestring(''.join(lines[1:-1]))

def ber_dec(data):
    '''
    Execute a simple ber decoder
    '''
    def tlv(s):
        try:
            tag = s.next()
        except StopIteration:
            return {}

        if ord(tag) & 0x1f == 0x1f:
            tag += s.next()
        while ord(tag[-1]) & 0x80 == 0x80: tag += s.next()

        length = ord(s.next())
        if length & 0x80 == 0x80:
            lendata = "".join([s.next() for i in range(length & 0x7f)])
            length = int(binascii.b2a_hex(lendata), 16)

        value = "".join([s.next() for i in range(length)])
        return {binascii.b2a_hex(tag): value}

    seq = (b for b in data)
    rv = {}
    while True:
      d = tlv(seq)
      if not d: break
      rv.update(d)

    import pprint
    pprint.pprint(rv)

if __name__ == '__main__':
    ber_dec(prep_base(sys.argv[1]))
