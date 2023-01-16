
# import hashlib
# import pyotp
# import time
# from Crypto.Cipher import DES
# import os
# import sys, getopt

# # hash_object = hashlib.sha256(b'Hello World')
# # hex_dig = hash_object.hexdigest()       #lấy mã hex đại diện của chuỗi hash đó
# # # dig_byte = hash_object.digest()       lấy chuỗi bytes
# # print(hex_dig)



# # totp = pyotp.TOTP('base32secret3232')

# # count = 0
# # while(count < 3):
# #     print(totp.now())# => 6 digits number

# #     # OTP verified for current time
    
# #     if (totp.verify(input('nhap ma OPT: '))) == True:
# #         print('thanh cong')
# #         break
# #     else:
# #         count += 1


# # totp = pyotp.TOTP("JBSWY3DPEHPK3PXP")
# # print("Current OTP: %s" % totp.now())

# # base32secret = 'S3K3TPI5MYA2M67V'
# # print('Secret:', base32secret)






# last_modified = time.ctime(os.path.getmtime('De bai.txt'))
# print(last_modified)

# key = last_modified + 'realkey' 

# hash_object = hashlib.sha256(key.encode('utf-8'))
# hex_dig = hash_object.hexdigest()       #lấy mã hex đại diện của chuỗi hash đó
# # dig_byte = hash_object.digest()       lấy chuỗi bytes
# print(hex_dig)

# now_time = time.ctime()
# hash_object = hashlib.sha256(now_time.encode('utf-8'))
# hex_dig2 = hash_object.hexdigest() 
# print(hex_dig2)



import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

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
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        l = self.bs - len(s) % self.bs
        return (s + l * chr(l).encode())

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

key = 'test'
obj = AESCipher(key)
with open('De bai.txt', 'rb') as f:
    enc = obj.encrypt(f.read())
with open('Debai_decrypted.txt', 'wb') as f2:
    dec = obj.decrypt(enc)
    f2.write(dec.encode('utf-8'))



