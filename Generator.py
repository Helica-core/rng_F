#!/usr/bin/env python
#
#
#
#
#

from Crypto.Cipher import AES
import hashlib

def hexdump(src, length=16):
    """
    """

    result = []
    digits = 4 if isinstance(src, unicode) else 2

    for i in xrange(0, len(src), length):
        s = src[i:i+length]
        hexa = b' '.join(["%0*X" % (digits, ord(x))  for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append(b"%04X    %-*s    %s" % (i, length*(digits + 1), hexa, text))
    
    print b'\n'.join(result)

def Expand2Bin(C, n): #n bits
    """
    """
    
    s = bin(C)[2:]

    rtn = ''

    if len(s) < n:
        
        s = (n-len(s)) * '0' + s
    
    for i in range(n/8):

        tmp = s[i*8 : i*8 + 8]
        
        rtn += chr(int(tmp,2))

    return rtn


def hexs2chrs(k):
    """ Change hex string to chr string
        LIKE:
                '5a2b2f' ---> b'\x5a\x2b\x2f'
    """

    rtn = ''

    for i in range(len(k)/2):
        
        rtn += chr(int(k[i*2:i*2+2],16))
        
    return rtn


def ord2hex(s):
    """ Change chr string to hex string
        LIKE:
                b'\x5a\x2b\x2f' ---> '5a2b2f'
        
    """

    return ''.join(['%02X' % ord(x)  for x in s])
 

class Generator:
    """ Generator class
    """    

    G_STATE = {'K':'','C':0}

    def __init__(self):
        
        self.InitializeGenerator()

        pass


    def InitializeGenerator(self):
        """
        """
    
        self.G_STATE['K'] = ''

        self.G_STATE['C'] = 0
        
    
    def ReSeed(self, seed):
        """
        """
        
        sha256 = hashlib.sha256()

        sha256.update(self.G_STATE['K'] + seed)

        self.G_STATE['K'] = hexs2chrs(sha256.hexdigest())

        self.G_STATE['C'] +=  1

        return self.G_STATE

    def GenerateBlocks(self, k):
        """
        """

        assert self.G_STATE['C'] != 0

        r = ''
        
        #ctr = Counter.new(nbits=128,initial_value=self.G_STATE['C'])
        
        #self.DisplayG()
        
        cipher = AES.new(self.G_STATE['K'], AES.MODE_ECB)
        
        for i in range(k):

            r += cipher.encrypt(Expand2Bin(self.G_STATE['C'], 128)) 
            
            self.G_STATE['C'] += 1
        
        #print '[+] AES result:'
        #print hexdump(r)
         
        return r
            
    def PseudoRandomData(self, n):
        """
        """
        
        assert n >= 0
        assert n <= 2**20
        
        #self.DisplayG()
        
        r = self.GenerateBlocks(n/16 + (n%16!=0))[0:n]

        self.G_STATE['K'] = self.GenerateBlocks(2)

        return r

    def DisplayG(self):

        print '\033[1;34m[---------------------------Generator State---------------------------------]'
       
        print '[+] Key:'
        print hexdump(self.G_STATE['K'])

        print '[+] Counter: %d' % self.G_STATE['C']

        print '[---------------------------------------------------------------------------]\n'
        print '\033[0m'
if __name__ == "__main__":

    gen = Generator()

    gen.ReSeed('pass pwaa')

    rd = gen.PseudoRandomData(1000)

    print '[+] Random Data'

    print hexdump(rd)

    gen.DisplayG()
