
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
import os
import random
import sys, getopt
import pyotp

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
        #độ dài cần padding cho đủ 
        l = self.bs - len(s) % self.bs 
        
        #pad random --> thay đổi độ dài cipher   | l + 6*16 < 127          
        r = Random.get_random_bytes(l - 1) + random.randint(0, 6)*Random.get_random_bytes(self.bs)

        #1 bytes cuối dùng để lưu độ dài pad   
        pad_len = len(r) + 1
        r += chr(pad_len).encode() 

        return s + r

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]



def encrypt_file(ifile, key):
    obj = AESCipher(key)
    with open(ifile, 'rb') as f:
        enc = obj.encrypt(f.read())
    os.remove(ifile)
    with open(ifile + '.enc', 'wb') as f:
        f.write(enc)

def decrypt_file(encfile, key):
    obj = AESCipher(key)
    with open(encfile, 'rb') as f:
        dec = obj.decrypt(f.read())
    os.remove(encfile)
    with open(encfile[:-4], 'wb') as f:
        f.write(dec)

def OTP():
    totp = pyotp.TOTP('base32secret3232')
    count = 0
    print('OPT code will change after 30s')
    while(count < 3):
        print('your OTP code: %s' % totp.now())# => 6 digits number

        # OTP verified for current time
        
        if (totp.verify(input('verify OPT code: '))) == True:
            return True
        else:
            count += 1
    return False

def main(argv):
    ifile = ''
    key = ''
    mode = ''

    try:
        opts, args = getopt.getopt(argv,"hi:k:m:",["ifile=","key=","mode="])   #sau dau :/= bat buoc phai co gia tri
    except getopt.GetoptError:
        print('1712603.py -i <filename> -k <key> -m <mode: e/d>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('1712603.py -i <filename> -k <key> -m <mode: e/d>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            filename = arg
        elif opt in ("-k", "--key"):
            key = arg
        elif opt in ("-m", "--mode"):
            mode = arg
    if mode == 'e':
        if OTP():
            encrypt_file(filename,key)
            print('check file.enc in current working directory')
        else:
            sys.exit(2)
    elif mode == 'd':
        if OTP():
            decrypt_file(filename,key)
            print('decrypted')
        else:
            sys.exit(2)
    else:
        print('1712603.py -i <filename> -k <key> -m <mode: e/d>')
        sys.exit(2)
    
    
if __name__ == "__main__":
   main(sys.argv[1:])



