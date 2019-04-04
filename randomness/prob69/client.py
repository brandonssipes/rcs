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
        port = int(sys.argv[1])
        mb = getpass.getpass("Bob password: ")
        b = Bob(mb,port)
        for i in range(256):
            b.first(i)
            b.second(i)
        chal = b.third()
        print(chal)
        exit(1)
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


class Bob:
    def __init__(self, m, port):
        self._mhash = hashlib.sha256(m.encode()).hexdigest()
        self._mInt = int(self._mhash, 16)
        self._xorm = str2bytes('',32) #make xorm a byte array

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', port)
        self.sock.connect(server_address)
        self.sock.send("hi\n".encode('utf8'))

    def first(self, i):
        b = (self._mInt >> i)%2
        #xx = [load(f) for f in ("x0", "x1")]
        xx = [0]*2
        xx[0] = self.sock.recv(1024)
        xx[1] = self.sock.recv(1024)
        #Enc = load("Enc")
        Enc = self.sock.recv(9999)
        rgen = Crypto.Random.new()

        bytelen = len(xx[0])
        pubkey = RSA.importKey(Enc)

        # Generate random nonce y and encrypted response u.
        # Have to iterate until both decryptions on the other end are less
        # than the modulus, expected O(1) times.
        while True:
            self._y = rgen.read(bytelen)
            try:
                u = xor(pubkey.encrypt(self._y, None)[0], xx[b])
                # this encryption is just to check the bounds of y
                pubkey.encrypt(xor(u, xx[1-b]), None)
                break
            except ValueError:
                pass

        #store('u', u)
        self.sock.send(u)

    def second(self, pos):
        #vv = [load(f) for f in ("v0", "v1")]
        vv = [0]*2
        vv[0] = self.sock.recv(1024)
        vv[1] = self.sock.recv(1024)
        self._xorm = xor(self._xorm, xor(self._y, vv[(self._mInt >> pos)%2]))
    
    def third(self):
        return self._xorm

if __name__ == '__main__':
    main()
