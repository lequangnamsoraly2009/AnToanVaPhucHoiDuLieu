
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
import os
import time

class AESCipher(object):

    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        if type(raw) != bytes:
            raw = raw.encode('utf-8')
        raw = self._pad(raw)                                                 
        iv = Random.new().read(AES.block_size)                                   
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def _pad(self, s):
        l = self.bs - len(s) % self.bs
        return (s + l * chr(l).encode()) #+ random 16x ky bytes

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

key = 'test'
ifile = 'test.txt'
encfile = 'test.txt.enc'
obj = AESCipher(key)



def encrypt_file(ifile):
    with open(ifile, 'rb') as f:
        enc = obj.encrypt(f.read())
    os.remove(ifile)
    with open(ifile + '.enc', 'wb') as f:
        f.write(enc)

def decrypt_file(encfile):
    with open(encfile, 'rb') as f:
        dec = obj.decrypt(f.read())
    os.remove(encfile)
    with open(encfile[:-4], 'wb') as f:
        f.write(dec)
