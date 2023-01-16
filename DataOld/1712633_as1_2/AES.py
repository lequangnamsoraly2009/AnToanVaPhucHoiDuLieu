import pyaes
import Crypto.Random
import base64
import sys, getopt
import ntpath
import hashlib
import random
import string


def CFB_MODE(PlainText_Bytes,aes_aray):
    iv=Crypto.Random.get_random_bytes(16)# lấy IV
    Cipher_Text=[]
    block_num=0 #biến đếm thứ tự block để tiện cho việc xử lý xor
    IV=aes_aray.encrypt(iv) #encrypt IV
    while block_num<len(PlainText_Bytes)/16: #bắt đầu vòng lặp xử lý CFB
        if block_num==0:
            for i in range(0,16): # xử lý 16 bytes (1 block)
                Cipher_Text.append(IV[i]^PlainText_Bytes[i])
            block_num=block_num+1
        else:#block thứ 2 trở đi
            temp_to_XOR=aes_aray.encrypt(Cipher_Text[(block_num-1)*16:block_num*16])
            for i in range(0,16):
                Cipher_Text.append(temp_to_XOR[i]^PlainText_Bytes[block_num*16+i])
            block_num=block_num+1
    return Cipher_Text,iv
def Padding(PlainText_Bytes):#em sử dụng padding khi lưu số bytes thêm vào ở bytes cuối cùng
    NumByteAdd=16-len(PlainText_Bytes)%16
    while(True):
        temp=random.randint(0,14)
        if int(temp)*16 <(255-16):
            NumByteAdd=NumByteAdd+int(temp)*16
            break
    for i in range(1,NumByteAdd+1):
        if i==NumByteAdd:
            PlainText_Bytes.append(NumByteAdd)
        else:
            temp=Crypto.Random.get_random_bytes(1)
            temp=int.from_bytes(temp,'little')
            PlainText_Bytes.append(temp)
    return
    
def RemovePadding(PlainText_Bytes):
    Num_Remove=PlainText_Bytes[len(PlainText_Bytes)-1]  
    for _ in range(0,Num_Remove):
        PlainText_Bytes.pop()
    return

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def savefileencode(bytestowrite,filename,fileloc):
    if fileloc=="":
        fileout=open(filename+'.cip','wb')
    else:
        fileout=open(fileloc+'/'+filename+'.cip','wb')
    temp=bytes(bytestowrite)
    fileout.write(temp)
    fileout.close()
    return 0
def savefiledecode(bytestowrite,filename,fileloc):
    if fileloc=="":
        fileout=open(filename,'wb')
    else:
        fileout=open(fileloc+'/'+filename,'wb')
    temp=bytes(bytestowrite)
    fileout.write(temp)
    fileout.close()
    return 0

def Encryption(Fileinloc,Key,Fileoutloc):
    keyhash=hashlib.md5(Key.encode())
    Key_32=bytes(keyhash.hexdigest(),"utf-8") 
    #separate plaintext to bytes of it
    filein=open(Fileinloc,'rb')
    PlainText_Bytes=list(filein.read())
    filein.close()
    Padding(PlainText_Bytes)
    #Initialization our aes
    aes_aray=pyaes.AES(Key_32)
    #Encrypt it
    Cipher_Text,IV=CFB_MODE(PlainText_Bytes,aes_aray)
    iv=base64.b64encode(IV)
    filename=path_leaf(Fileinloc)
    savefileencode(Cipher_Text+list(iv),filename,Fileoutloc)
    return 0



def Decryption(Fileenc,Key,Fileoutloc):
    keyhash=hashlib.md5(Key.encode())
    Key_32=bytes(keyhash.hexdigest(),"utf-8") 
    filein=open(Fileenc,'rb')
    Cipher_Text=list(filein.read())
    iv=Cipher_Text[-24:]
    Cipher_Text=Cipher_Text[:len(Cipher_Text)-24]
    iv=bytes(iv)
    IV=base64.b64decode(iv)
    aes_aray=pyaes.AES(Key_32)
    IV=aes_aray.encrypt(IV)
    block_num=0
    PlainText_Bytes=[]
    #phần này khá giống vs Encrypt
    while block_num<len(Cipher_Text)/16:
        if block_num==0:
            for i in range(0,16):
                PlainText_Bytes.append(IV[i]^Cipher_Text[i])
            block_num=block_num+1
        else:
            temp_to_XOR=aes_aray.encrypt(Cipher_Text[(block_num-1)*16:block_num*16])
            for i in range(0,16):
                PlainText_Bytes.append(temp_to_XOR[i]^Cipher_Text[block_num*16+i])
            block_num=block_num+1
    RemovePadding(PlainText_Bytes)
    
    filename=path_leaf(Fileenc)
    filename=filename[:len(filename)-4]
    savefiledecode(PlainText_Bytes,filename,Fileoutloc)
    return 0
def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str
def OTP():
    otp_pass=get_random_alphanumeric_string(8)
    print("this is your session otp: %s \nPlease insert your otp:" %otp_pass )
    pass_in=input()
    if pass_in==otp_pass:
        return True
    else:
        return False

def main(argv):
    infile=''
    outfile=''
    key=''
    mode=''
    try:
        opts, args = getopt.getopt(argv,"hi:ok:m:",["ifile=","ofile=","Key=","mode="])
    except getopt.GetoptError:
        print('AES.py -i <inputfile> -o <outputfile> -k <Key> -m <mode: e to encrypt/d to decrypt>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print( 'AES.py -i <inputfile> -o <outputfile> -k <Key> -m <mode: e to encrypt/d to decrypt>')
            sys.exit(2)
        elif opt in ("-i","--ifile"):
            infile=arg
        elif opt in ("-o","--ofile"):
            outfile=arg
        elif opt in ("-k","--Key"):
            key=arg
        elif opt in ("-m","--mode"):
            mode=arg
    if mode=="":
        print(argv[0]+ ' -i <inputfile> -o <outputfile> -k <Key> -m <mode: e to encrypt/d to decrypt>')
        print("mode is null error")
        sys.exit(2)
    elif infile=='':
        print(argv[0]+ ' -i <inputfile> -o <outputfile> -k <Key> -m <mode: e to encrypt/d to decrypt>')
        print("filein is null error")
        sys.exit(2)
    elif mode=='e':
        if OTP():
            Encryption(infile,key,outfile)
        else:
            print("wrong otp")
            sys.exit(2)
    elif mode=='d':
        if OTP():
            Decryption(infile,key,outfile)
        else:
            print("wrong otp")
            sys.exit(2)


if __name__=="__main__":
    main(sys.argv[1:])


    
    
        