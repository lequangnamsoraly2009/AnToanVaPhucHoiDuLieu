import os
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
import os
import random
import handle_raw_data as hrd


_root = 'test'

def get_vol_structure(_root = 'test'):
    a = ''
    b = ''
    for root, dirs, files in os.walk(_root):
        a += (root + '\\' + '\n')
        for name in files:
            a += (os.path.join(root, name) + '\n')
            b += (os.path.join(root, name) + '\n')


    paths = a.replace('\\','/')
    files = b.replace('\\','/')

    l = []
    for name in files.split('\n')[:-1]:
        with open(name, 'rb') as n:
            b_data = n.read() 
        l.append(b_data)

    paths_l = paths.split('\n')[:-1]
    count = 0
    for i in range(len(paths_l)):
        if paths_l[i][-1] == '/':
            paths_l[i] = (paths_l[i] + ',,')
        else:
            paths_l[i] = (paths_l[i] + ',' + str(l[count]) + ',')
            count+=1
    a = ''
    for i in paths_l:
        a+=(i+'\n')
    
    return a[:-1]

# -----------encrypt str-----------------------

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
        #độ dài cần pad cho đủ 
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

# ------------------------------
def make_vol(_root = 'test'):

    a = get_vol_structure(_root = _root)
    # --------------
    key = '12345678'
    obj = AESCipher(key)
    e_str = obj.encrypt(a)

    # -----------------

    with open(_root + '.vol','wb') as _r:
        _r.write(e_str)

def update_vol(r, new_data):
    newer_data = ''
    for e in new_data:
        newer_data += (e + '\n')
        # --------------
    key = '12345678'
    obj = AESCipher(key)
    e_str = obj.encrypt(newer_data[:-1])
    # -----------------update vol---------------
    with open(r,'wb') as _r:
        _r.write(e_str)
#--------------------------------
def get_raw_data(_root = 'test.vol'):
    with open(_root, 'rb') as f:
        b64 = f.read()
    
    # --------------------------------
    key = '12345678'
    obj = AESCipher(key)
    d_str = obj.decrypt(b64)
    # -------------------------------
    return (d_str.decode('utf=8'))  


def main():

    s = -1
    while s!= 0:
        print('''
        1. Make volume.
        2. Show list files.
        3. Set a password to a file.
        4. Export a file.
        5. Import a file.
        6. Delete a file.
        0: Exit
        ''') 
                   
        s = int(input('Your select: '))
       
        if s == 1:
            r = input('folder name: ')
            make_vol(_root=r)
            print('check '+r+'.vol in your current directory')
            input('press any key to continue....')
        elif s == 2:
            r = input('input vol-name: ')
            raw_data = get_raw_data(_root=r).split('\n')
            tree = hrd.Directory_tree(raw_data)
            print(tree)
            input('press any key to continue....')
        elif s == 3:
            r = input('input vol-name: ')
            raw_data = get_raw_data(_root=r).split('\n')
            tree = hrd.Directory_tree(raw_data)
            print(tree)
            path = input('input path: ')
            pwd = input('input password:')
            new_data = hrd.set_pwd(raw_data,pwd,path)
            update_vol(r,new_data)
            input('press any key to continue....')
        elif s == 4:
            r = input('input vol-name: ')
            raw_data = get_raw_data(_root=r).split('\n')
            tree = hrd.Directory_tree(raw_data)
            print(tree)
            path = input('input path: ')
            pwd = input('password(default: blank): ')
            ef = hrd.export_file(raw_data,pwd,path)
            
            # -----------------------------
            ef = ef.split(',')
            file_name = ''
            for i in range(len(ef[0]) - 1, -1 ,-1):
                if ef[0][i] == '/':
                    file_name = ef[0][i+1:]
                    break
            with open(file_name,'wb') as f:
                f.write(eval(ef[1]))
            print('check ',file_name,' in your current working directory')
            input('press any key to continue....')
        elif s == 5:
            file_name = input('import file\'s path: ')
            with open(file_name,'rb') as f:
                if_data = f.read()
            for i in range(len(file_name) - 1,-1,-1):
                if file_name[i] == '/':
                    file_name = file_name[i+1:]
                    break
            
            r = input('import to vol-name: ')
            raw_data = get_raw_data(_root=r).split('\n')
            tree = hrd.Directory_tree(raw_data)
            print(tree)

            folder_path = input('import to folder path: ')
            
            data_import = folder_path + file_name +','+ str(if_data) +','
            new_data = hrd.import_data(data_import, raw_data)
            if new_data == -1:
                print('error')
                input('press any key to continue....')
            else:
                print('import successful')
                update_vol(r,new_data)
                tree = hrd.Directory_tree(raw_data)
                print(tree)
                input('press any key to continue....')
        elif s == 6:
            r = input('import to vol-name: ')
            raw_data = get_raw_data(_root=r).split('\n')
            tree = hrd.Directory_tree(raw_data)
            print(tree)
            path = input('input target path: ')
            new_data = hrd.del_data(path, raw_data)
            if new_data == -1:
                print('error')
                input('press any key to continue....')
            else:
                print('delete successful')
                update_vol(r,new_data)
                tree = hrd.Directory_tree(raw_data)
                print(tree)
                input('press any key to continue....')
        elif s == 0:
            print('Exit...')
            break
        else:
            print('wrong input')

if __name__ == "__main__":
    main()

# print(get_raw_data('test.vol'))