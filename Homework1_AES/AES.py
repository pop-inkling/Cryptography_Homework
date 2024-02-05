import numpy as np
from s_box import generate_sbox, generate_inv_sbox
from key import KeyExtend, generate_key
from trans import Row_Shift, Col_Fusion, Row_inv_Shift, Col_inv_Fusion
from bytes import str2array_Plain, array2str_base64, str2array_base64



def AES_Encode(Texts):
        
        sbox = generate_sbox() # 生成S盒
        Plaintext = str2array_Plain(Texts) # 将明文变为16个字节一组的数组
        Ciphertext = np.zeros(Plaintext.shape,dtype=int)
        Key = generate_key()
        Keywords = KeyExtend(Key) # 密钥扩展

        # 对明文中的每一组进行加密
        for m in range(Plaintext.shape[0]):
                plaintext_square = Plaintext[m].reshape(4,4,order='F')

                plaintext_square = plaintext_square ^ Keywords[:,0:4] # 密钥异或

                # Round 1~9
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
                
                # Round 10
                for i in range(4):
                        for j in range(4):
                                temp = plaintext_square[i,j]
                                plaintext_square[i,j] = sbox[temp>>4,temp&0x0F]

                plaintext_square = Row_Shift(plaintext_square)

                plaintext_square = plaintext_square ^ Keywords[:,40:44]

                Ciphertext[m] = plaintext_square.reshape(16,order='F') 

        Ciphertext = Ciphertext.reshape(-1)
        
        
        Ciphertext=array2str_base64(Ciphertext) # 将密文进行base64编码，便于展示

        Key_string = array2str_base64(Key) # 密钥与密文同理

        return Ciphertext,Key_string

def AES_Decode(Ciphertext,Key):
        
        # 将得到的密钥和密文进行base64解码
        Ciphertext = str2array_base64(Ciphertext)
        Key = str2array_base64(Key)

        Ciphertext = Ciphertext.reshape(-1,16) # 16个字节一组进行分组

        Keywords = KeyExtend(Key)
        Plaintext = np.zeros(Ciphertext.shape,dtype=int)
        inv_sbox = generate_inv_sbox()

        for m in range(Ciphertext.shape[0]):
                Ciphertext_square = Ciphertext[m].reshape(4,4,order='F')

                Ciphertext_square = Ciphertext_square ^ Keywords[:,40:44]
                
                # Round 1~9
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

                # Round 10
                for i in range(4):
                        for j in range(4):
                                temp = Ciphertext_square[i,j]
                                Ciphertext_square[i,j] = inv_sbox[temp>>4,temp&0x0F]

                Ciphertext_square = Ciphertext_square ^ Keywords[:,0:4]
                Plaintext[m] = Ciphertext_square.reshape(16,order='F')
        
        # 格式修改
        Plaintext = Plaintext.reshape(-1)

        Plaintext = Plaintext.astype(np.uint8)
        Plaintext = Plaintext.tobytes()

        Plaintext = Plaintext.rstrip(b'\x00') # 去掉加密时填充的字节'\x00'

        text = Plaintext.decode('utf-8')

        return text

        