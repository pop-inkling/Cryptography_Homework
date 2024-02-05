from random import randint,randrange

# 快速幂运算（模n）
def FastExpMod(g,n,mod):
    result = 1
    a = g
    n = int(n)
    while(n != 0):
        if(n&0b1 == 1):
            result = (result * a) % mod
        
        a = (a * a) % mod

        n = n>>1
    
    return result

# miller-rabin素性检测
def miller_rabin_test(n):
    q = n-1
    k = 0
    while(q%2==0):
        k += 1
        q = q/2
    a = randint(2,n-2)
    if(FastExpMod(a,q,n)==1):
        return True
    
    for i in range(k):
        if(FastExpMod(a,((2**i)*q),n)==n-1):
            return True
    
    return False

# 生成length位的大素数
def create_prime_number(length):
    while True:
        all_num = '123456789'
        random_num = ''
        index = randint(0,8)
        random_num += all_num[index]
        all_num += '0'

        for _ in range(length-2):
            index = randint(0,9)
            random_num += all_num[index]

        index = randrange(0,9,2)
        random_num += all_num[index]

        result = True
        for _ in range(10):
            if(miller_rabin_test(int(random_num))):
                pass
            else:
                result = False
                break
        if result:
            return int(random_num)

# 欧几里得算法
def Euclid(a,b):
    if(b == 0):
        return a
    else:
        return Euclid(b,a%b)
  
# 扩展欧几里得算法
def Extend_Euclid(a,b):
    xinv1, yinv1 = 1, 0
    x0, y0 = 0, 1
    x1, y1 = 0, 0
    r = a % b
    q = (a-r) / b
    temp = a
    while(r!=0):
        x1 = xinv1-q*x0
        y1 = yinv1-q*y0
        xinv1, yinv1 = x0, y0
        x0, y0 = x1, y1
        a = b
        b = r
        r = a % b
        q = (a-r) / b
    
    if(y0<0):
        y0 +=temp
    if(x0<0):
        x0 +=temp
    return int(y0) 

# 选择一个与Phi(n)互素的e
def select_e(phi_n):
    while True:
        e = randint(2,phi_n-1)
        if(Euclid(phi_n,e) == 1):
            return e

# 生成公钥、私钥、公开模数
def create_keys(key_length):
    p = create_prime_number(key_length)
    q = create_prime_number(key_length)

    n = p*q
    phi_n = (p-1)*(q-1)
    e = select_e(phi_n)
    d = Extend_Euclid(phi_n,e)

    return int(n), int(e), int(d)
