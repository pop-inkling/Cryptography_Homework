import numpy as np
from s_box import generate_sbox, generate_inv_sbox
from key import KeyExtend, generate_key
from trans import Row_Shift, Col_Fusion, Row_inv_Shift, Col_inv_Fusion
from bytes import str2array_Plain, array2str_base64, str2array_base64



def AES_Encode(Texts):
        # Texts = 我想测试一下AES的性能
        # Plaintext = np.array([[0x01,0x23,0x45,0x67,0x89,0xab,0xcd,0xef,0xfe,0xdc,0xba,0x98,0x76,0x54,0x32,0x10]])
        #Texts = input('请输入需要加密的信息：')
        sbox = generate_sbox()
        Plaintext = str2array_Plain(Texts)
        Ciphertext = np.zeros(Plaintext.shape,dtype=int)
        # Key = np.array([0x0f,0x15,0x71,0xc9,0x47,0xd9,0xe8,0x59,0x0c,0xb7,0xad,0xd6,0xaf,0x7f,0x67,0x98])
        Key = generate_key()
        Keywords = KeyExtend(Key)

        # for i in range(4):
        #         # print(f'{sbox[i,j]:02x}') 
        #         print(' '.join(f'{Keywords[i,j]:02x}' for j in range(44)))
        for m in range(Plaintext.shape[0]):
                plaintext_square = Plaintext[m].reshape(4,4,order='F')

                plaintext_square = plaintext_square ^ Keywords[:,0:4]

                for k in range(1,10):
                        # S盒替换
                        for i in range(4):
                                for j in range(4):
                                        temp = plaintext_square[i,j]
                                        plaintext_square[i,j] = sbox[temp>>4,temp&0x0F]
                        # 行移位    
                        plaintext_square = Row_Shift(plaintext_square)
                        # 列混淆
                        plaintext_square = Col_Fusion(plaintext_square)
                        # 密钥异或
                        plaintext_square = plaintext_square ^ Keywords[:,4*k:4*k+4]
                
                for i in range(4):
                        for j in range(4):
                                temp = plaintext_square[i,j]
                                plaintext_square[i,j] = sbox[temp>>4,temp&0x0F]

                plaintext_square = Row_Shift(plaintext_square)

                plaintext_square = plaintext_square ^ Keywords[:,40:44]

                Ciphertext[m] = plaintext_square.reshape(16,order='F')

        # for i in range(Ciphertext.shape[0]):
        #         print(' '.join(f'{Ciphertext[i,j]:02x}' for j in range(Ciphertext.shape[1])))
        Ciphertext = Ciphertext.reshape(-1)
        # print(' '.join(f'{Ciphertext[j]:02x}' for j in range(Ciphertext.shape[0])))
        Ciphertext=array2str_base64(Ciphertext)
        # print("加密后的密文为："+Ciphertext)

        Key_string = array2str_base64(Key)
        # print("密钥为："+Key_string)

        return Ciphertext,Key_string

def AES_Decode(Ciphertext,Key):
# 加密后的密文为：YcowDFTJpKxu410cyiZAj43uODoCs4qazQVTyUo4v6o=
# 密钥为：UAklypumHRIGt6uVTfWxfA==

        # Ciphertext = input("请输入需解密的密文：")
        # Key = input("请输入对应密钥：")

        # Ciphertext = '/wuESghTv3xpNKtDZBSPuQ=='
        # Key = 'DxVxyUfZ6FkMt63Wr39nmA=='
        Ciphertext = str2array_base64(Ciphertext)
        Key = str2array_base64(Key)

        # print(' '.join(f'{Ciphertext[j]:02x}' for j in range(Ciphertext.shape[0])))
        # print(' '.join(f'{Key[j]:02x}' for j in range(16)))

        Ciphertext = Ciphertext.reshape(-1,16)

        # for i in range(2):
        #         print(' '.join(f'{Ciphertext[i,j]:02x}' for j in range(16)))

        Keywords = KeyExtend(Key)
        Plaintext = np.zeros(Ciphertext.shape,dtype=int)
        inv_sbox = generate_inv_sbox()

        for m in range(Ciphertext.shape[0]):
                Ciphertext_square = Ciphertext[m].reshape(4,4,order='F')

                Ciphertext_square = Ciphertext_square ^ Keywords[:,40:44]

                for k in range(1,10):
                        # 逆行移位
                        Ciphertext_square = Row_inv_Shift(Ciphertext_square)
                        # 逆S盒替换
                        for i in range(4):
                                for j in range(4):
                                        temp = Ciphertext_square[i,j]
                                        Ciphertext_square[i,j] = inv_sbox[temp>>4,temp&0x0F]
                        # 逆密钥异或
                        Ciphertext_square = Ciphertext_square ^ Keywords[:,(40-4*k):(44-4*k)]
                        # 逆列混淆
                        Ciphertext_square = Col_inv_Fusion(Ciphertext_square)
                
                Ciphertext_square = Row_inv_Shift(Ciphertext_square)

                for i in range(4):
                        for j in range(4):
                                temp = Ciphertext_square[i,j]
                                Ciphertext_square[i,j] = inv_sbox[temp>>4,temp&0x0F]

                Ciphertext_square = Ciphertext_square ^ Keywords[:,0:4]
                Plaintext[m] = Ciphertext_square.reshape(16,order='F')

        Plaintext = Plaintext.reshape(-1)

        # print(' '.join(f'{Plaintext[j]:02x}' for j in range(16)))
        Plaintext = Plaintext.astype(np.uint8)
        Plaintext = Plaintext.tobytes()
        # print(Plaintext)
        Plaintext = Plaintext.rstrip(b'\x00')
        # print(Plaintext)
        text = Plaintext.decode('utf-8')
        # print(text)
        return text

        