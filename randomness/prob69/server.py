#!/usr/bin/env python3

# 1-2 Oblivious Transfer algorithm using files
# SI 486D Spring 2016
#Brandon Sipes

import socket
import sys
import getpass
import Crypto.Random
import Crypto.PublicKey.RSA as RSA
import hashlib
import secrets

def main():
    if len(sys.argv) == 2:
        ma = getpass.getpass("Alice password: ")
        port = int(sys.argv[1])
        a = Alice(ma,port)
        for i in range(256):
            a.first()
            a.second(i)
    else:
        print("ERROR: Please enter a port number.")
        exit(1)

def str2bytes(s, n):
    """Encodes string s into exactly n bytes."""
    res = s.encode('utf8')
    if len(res) > n:
        print("ERROR: message is too long to encode in", n, "bytes")
        exit(1)
    # pad with 0 bytes to make length exactly n
    return res +  b'\0' * (n - len(res))

def bytes2str(b):
    """Decodes bytes back to string, removing any padding null bytes."""
    return b.decode('utf8').rstrip('\0')

def xor(b1, b2):
    """Performs byte-wise XOR on two bytes objects"""
    return bytes(a^b for (a,b) in zip(b1, b2))

def load(fname):
    """Reads a file and returns bytes of its contents"""
    try:
        with open(fname, 'rb') as fin:
            return fin.read()
    except FileNotFoundError:
        print("Couldn't read file", fname)
        exit(1)

def store(fname, data):
    """Stores bytes data into a file with the given name."""
    with open(fname, 'wb') as fout:
        fout.write(data)

class Alice:
    def __init__(self, m, port, modlen=1024):
        self._modlen = modlen
        bytelen = self._modlen // 8
        self._mb = str2bytes(m, bytelen)
        self._mhash = hashlib.sha256(m.encode()).hexdigest()
        self._mInt = int(self._mhash, 16)
        a = secrets.token_bytes(16) #16 bytes is 128 bits
        lead = str2bytes('',16) #lead padds out with zeros so this is 128 zeros
        challenge = lead + a #to get 256 bits
        self.nonce = [[0 for x in range(2)] for y in range(256)] #double nonce array 2 by 256
        xorm = challenge #xor starts off and ends up as challenge
        for i in range(0,255):
            self.nonce[i][0] = secrets.token_bytes(32)
            self.nonce[i][1] = secrets.token_bytes(32)
            xorm = xor(xorm, self.nonce[i][(self._mInt >> i)%2]) #I think this works
        self.nonce[255][0] = secrets.token_bytes(32) #fill last two with garabge
        self.nonce[255][1] = secrets.token_bytes(32)
        self.nonce[255][(self._mInt >> 255)%2] = xorm #overwrite with xor of everything else

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', port)
        sock.bind(server_address)
        sock.listen(1)

        while True:
            # Wait for a connection
            self.connection, self.client_address = sock.accept()
            break





    def first(self):
        rgen = Crypto.Random.new()

        # Generate key-pair.
        # The top 2 bits of the RSA modulus must both equal 1.
        # This loop executes expected O(1) times to find such a modulus.
        while True:
            self._keys = RSA.generate(self._modlen, rgen.read)
            if self._keys.n >> (self._modlen - 2) == 3:
                break

        bytelen = self._modlen // 8
        self._x0 = rgen.read(bytelen)
        self._x1 = rgen.read(bytelen)

        self.connection.send(self._x0)
        self.connection.send(self._x1)
        self.connection.send(self._keys.publickey().exportKey('DER'))
        #store("x0", self._x0)
        #store("x1", self._x1)
        #store("Enc", self._keys.publickey().exportKey('DER'))

    def second(self, pos):
        #u = load("u")
        u = self.connection.recv(1024)

        v0 = xor(self._keys.decrypt(xor(u, self._x0)), self.nonce[pos][0])
        v1 = xor(self._keys.decrypt(xor(u, self._x1)), self.nonce[pos][1])

        #store("v0", v0)
        #store("v1", v1)
        self.connection.send(v0)
        self.connection.send(v1)

if __name__ == '__main__':
    main()
