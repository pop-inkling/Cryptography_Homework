import numpy as np
from s_box import poly_multi

## 列混淆变换
#对一列进行混淆
def Mix_Col(text):

    temp = np.zeros(4,dtype=int)
    temp[0] = poly_multi(0x02,text[0]) ^ poly_multi(0x03,text[1]) ^ text[2] ^ text[3]
    temp[1] = text[0] ^ poly_multi(0x02,text[1]) ^ poly_multi(0x03,text[2]) ^ text[3]
    temp[2] = text[0] ^ text[1] ^ poly_multi(0x02,text[2]) ^ poly_multi(0x03,text[3])
    temp[3] = poly_multi(0x03,text[0]) ^ text[1] ^ text[2] ^ poly_multi(0x02,text[3])

    return temp

def Mix_inv_Col(text):

    temp = np.zeros(4,dtype=int)
    temp[0] = poly_multi(0x0E,text[0]) ^ poly_multi(0x0B,text[1]) ^ poly_multi(0x0D,text[2]) ^ poly_multi(0x09,text[3])
    temp[1] = poly_multi(0x09,text[0]) ^ poly_multi(0x0E,text[1]) ^ poly_multi(0x0B,text[2]) ^ poly_multi(0x0D,text[3])
    temp[2] = poly_multi(0x0D,text[0]) ^ poly_multi(0x09,text[1]) ^ poly_multi(0x0E,text[2]) ^ poly_multi(0x0B,text[3])
    temp[3] = poly_multi(0x0B,text[0]) ^ poly_multi(0x0D,text[1]) ^ poly_multi(0x09,text[2]) ^ poly_multi(0x0E,text[3])

    return temp
#对整个矩阵进行混淆
def Col_Fusion(texts):
    for i in range(4):
        texts[:,i] = Mix_Col(texts[:,i])
    return texts

def Col_inv_Fusion(texts):
    for i in range(4):
        texts[:,i] = Mix_inv_Col(texts[:,i])
    return texts
## 行移位变换
# 左移位变换
def Left_Shift(text,bit):
    length = np.size(text)
    shift_text = np.zeros(length,dtype=int)
    shift_text[0:length-bit] = text[bit:length]
    shift_text[length-bit:length] = text[0:bit]

    return shift_text

# print(Left_Shift(np.array([2,3,1,1,3,5,6,7]),3))
# 右移位变换
def Right_Shift(text,bit):
    length = np.size(text)
    shift_text = np.zeros(length,dtype=int)
    shift_text[0:bit] = text[length-bit:length]
    shift_text[bit:length] = text[0:length-bit]

    return shift_text

# print(Right_Shift(np.array([2,3,1,1,3,5,6,7]),3))

def Row_Shift(texts):
    for i in range(1,4):
        texts[i] = Left_Shift(texts[i],i)
    
    return texts

def Row_inv_Shift(texts):
    for i in range(1,4):
        texts[i] = Right_Shift(texts[i],i)

    return texts