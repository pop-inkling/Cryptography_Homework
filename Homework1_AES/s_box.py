import numpy as np

# 初始化S盒
def initalize_sbox():
    sbox = np.ones((16,16),dtype = int) #用np.ones 函数生成16×16矩阵

    for i in range(16):
        for j in range(16):
            sbox[i,j] = i<<4|j
    
    return sbox   

#当前多项式的最高项
def find_high(a):    
    i = 0
    while(a!=0):
        i+=1
        a=a>>1
    return i-1

# 多项式除法
def poly_div(a,b):

    b_len = find_high(b)
    a_len = find_high(a)
    q, r = 0, 0 #q为商，r为余数
    
    while(a_len>=b_len):
        q += 1<<(a_len-b_len)
        r = a ^ (b<<(a_len-b_len))
        a = r
        a_len = find_high(a)
    return q, r

# 该乘法默认为GF(2^8)内的乘法   
def poly_multi(a,b,c=0b100011011):
    temp = 0
    for i in range(find_high(b)+1):
        if((b>>i)&0b1 == 0b1):
            temp ^= a<<i
    if(find_high(temp)>=find_high(c)):
         q,temp = poly_div(temp,c)

    return temp

# 多项式扩展欧几里得算法
def Poly_Extend_Euclid(a,b):
    xinv1, yinv1 = 1, 0
    x0, y0 = 0, 1
    x1, y1 = 0, 0
    q, r = poly_div(a,b)
    while(r!=0):
        x1 = xinv1^poly_multi(q,x0)
        y1 = yinv1^poly_multi(q,y0)
        xinv1, yinv1 = x0, y0
        x0, y0 = x1, y1
        a = b
        b = r
        q, r = poly_div(a,b)
    return y0

# 字节变换
def byte_trans(num,c):
     result = 0
     for i in range(8):
          result += (((num>>i)&0x1) ^ ((num>>((i+4)%8))&0x1) ^ ((num>>((i+5)%8))&0x1) \
                    ^ ((num>>((i+6)%8))&0x1) ^ ((num>>((i+7)%8))&0x1) ^ ((c>>i)&0x1)) <<i
     return result

# 逆字节变换
def byte_inv_trans(num,c):
    result = 0
    for i in range(8):
        result += (((num>>((i+2)%8))&0x1) ^ ((num>>((i+5)%8))&0x1) ^ ((num>>((i+7)%8))&0x1) ^ ((c>>i)&0x1)) <<i
    return result
        
# 生成S盒
def generate_sbox():
    sbox = initalize_sbox()
    
    for i in range(16):
         for j in range(16):
              if(sbox[i,j] == 0x00):
                  sbox[i,j] = byte_trans(sbox[i,j],0x63)
              else:
                  sbox[i,j] = Poly_Extend_Euclid(0b100011011,sbox[i,j])
                  sbox[i,j] = byte_trans(sbox[i,j],0x63)
              
    return sbox

# 生成逆S盒
def generate_inv_sbox():
    sbox = initalize_sbox()

    for i in range(16):
        for j in range(16):
                sbox[i,j] = byte_inv_trans(sbox[i,j],0x05)
                if(sbox[i,j] != 0x00):
                     sbox[i,j] = Poly_Extend_Euclid(0b100011011,sbox[i,j])
                
    return sbox