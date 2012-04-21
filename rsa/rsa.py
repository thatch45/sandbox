'''
Wrap the stuff pycrypto needs for reading rsa keys
'''

# Import python docs
import sys
import base64
import binascii
import struct

# Import PyCrypto
from Crypto.PublicKey import RSA

def prep_base(path):
    '''
    Prep the base64 data from a key
    '''
    # This should manage more types of pem formatted keys
    lines = open(path, 'r').readlines()
    return base64.decodestring(''.join(lines[1:-1]))

def inflate_long(s, always_positive=False):
    '''
    Turns a normalized byte string into a long-int (adapted from
    Crypto.Util.number)
    '''
    out = 0L
    negative = 0
    if not always_positive and (len(s) > 0) and (ord(s[0]) >= 0x80):
        negative = 1
    if len(s) % 4:
        filler = '\x00'
        if negative:
            filler = '\xff'
        s = filler * (4 - len(s) % 4) + s
    for i in range(0, len(s), 4):
        out = (out << 32) + struct.unpack('>I', s[i:i+4])[0]
    if negative:
        out -= (1L << (8 * len(s)))
    return out

def deflate_long(n, add_sign_padding=True):
    '''
    turns a long-int into a normalized byte string (adapted from
    Crypto.Util.number)
    '''
    # after much testing, this algorithm was deemed to be the fastest
    s = ''
    n = long(n)
    while (n != 0) and (n != -1):
        s = struct.pack('>I', n & 0xffffffffL) + s
        n = n >> 32
    # strip off leading zeros, FFs
    for i in enumerate(s):
        if (n == 0) and (i[1] != '\000'):
            break
        if (n == -1) and (i[1] != '\xff'):
            break
    else:
        # degenerate case, n was either 0 or -1
        i = (0,)
        if n == 0:
            s = '\000'
        else:
            s = '\xff'
    s = s[i[0]:]
    if add_sign_padding:
        if (n == 0) and (ord(s[0]) >= 0x80):
            s = '\x00' + s
        if (n == -1) and (ord(s[0]) < 0x80):
            s = '\xff' + s
    return s

class BERException (Exception):
    pass


class BER(object):
    '''
    Decode a simple BER for an rsa key
    '''
    def __init__(self, content=''):
        self.content = content
        self.idx = 0

    def decode(self):
        return self.decode_next()
    
    def decode_next(self):
        if self.idx >= len(self.content):
            return None
        ident = ord(self.content[self.idx])
        self.idx += 1
        if (ident & 31) == 31:
            # identifier > 30
            ident = 0
            while self.idx < len(self.content):
                t = ord(self.content[self.idx])
                self.idx += 1
                ident = (ident << 7) | (t & 0x7f)
                if not (t & 0x80):
                    break
        if self.idx >= len(self.content):
            return None
        # now fetch length
        size = ord(self.content[self.idx])
        self.idx += 1
        if size & 0x80:
            t = size & 0x7f
            if self.idx + t > len(self.content):
                return None
            size = inflate_long(self.content[self.idx : self.idx + t], True)
            self.idx += t
        if self.idx + size > len(self.content):
            # can't fit
            return None
        data = self.content[self.idx : self.idx + size]
        self.idx += size
        # now switch on id
        if ident == 0x30:
            # sequence
            return self.decode_sequence(data)
        elif ident == 2:
            # int
            return inflate_long(data)
        else:
            # 1: boolean (00 false, otherwise true)
            raise BERException('Unknown ber encoding type {0}'.format(ident))

    def decode_sequence(data):
        out = []
        b = BER(data)
        while True:
            x = b.decode_next()
            if x is None:
                break
            out.append(x)
        return out
    decode_sequence = staticmethod(decode_sequence)

    def encode_tlv(self, ident, val):
        # no need to support ident > 31 here
        self.content += chr(ident)
        if len(val) > 0x7f:
            lenstr = deflate_long(len(val))
            self.content += chr(0x80 + len(lenstr)) + lenstr
        else:
            self.content += chr(len(val))
        self.content += val

    def encode(self, x):
        if type(x) is bool:
            if x:
                self.encode_tlv(1, '\xff')
            else:
                self.encode_tlv(1, '\x00')
        elif (type(x) is int) or (type(x) is long):
            self.encode_tlv(2, deflate_long(x))
        elif type(x) is str:
            self.encode_tlv(4, x)
        elif (type(x) is list) or (type(x) is tuple):
            self.encode_tlv(0x30, self.encode_sequence(x))
        else:
            raise BERException('Unknown type for encoding: {0}'.format(repr(type(x))))

    def encode_sequence(data):
        b = BER()
        for item in data:
            b.encode(item)
        return str(b)
    encode_sequence = staticmethod(encode_sequence)


if __name__ == '__main__':
    keylist = BER(prep_base(sys.argv[1])).decode()
    print keylist






