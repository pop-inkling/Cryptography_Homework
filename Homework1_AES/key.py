import numpy as np
import s_box
from random import randint

sbox = s_box.generate_sbox()

# 密钥扩展中的g函数
def g_function(words, turn):
    word = words*1
    #第一步 字循环
    temp = word[0]
    for i in range(3):
        word[i] = word[i+1]
    word[3] = temp
    #第二步 字代替
    for i in range(4):
        temp = word[i]
        word[i] = sbox[temp>>4,temp&0x0F]
    #第三步 异或
    RCj = s_box.poly_multi(pow(2,turn-1),0x01)
    costant = np.zeros(4,dtype=int)
    costant[0] = RCj
    word = word^costant

    return word

# 密钥扩展
def KeyExtend(key):
    words = np.ones((4,44),dtype=int)
    key = key.reshape(4,4,order='F')
    for i in range(4):
        words[:,i] = key[:,i]

    for i in range(1,11):
        temp = g_function(words[:,4*i-1],i)
        words[:,4*i] = words[:,4*i-4]^temp
        for j in range(3):
            words[:,4*i+j+1] = words[:,4*i+j]^words[:,4*i+j-3]
    
    return words

# 生成随机128位密钥
def generate_key():
    key = np.ones(16,dtype=int)
    for i in range(16):
        key[i] = randint(0,255)
    
    key = key.astype(np.uint8)

    return key