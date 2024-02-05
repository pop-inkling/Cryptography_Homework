from bytes import str2array_Plain, int_to_bytes, bytes_to_int, byte2str_base64, str2byte_base64, split_bytes
from prime_num import FastExpMod

def RSA_Encrypt(text,public_key,modulus):
    byte_length = 8
    plaintext = str2array_Plain(text)
    length = len(plaintext)
    ciphertext = list(range(length))
    
    # RSA加密
    for i in range(length):
        ciphertext[i] = FastExpMod(plaintext[i],public_key,modulus)
    
    # 数字变为字节
    ciphertext_bytes = list(range(length))
    for i in range(length):
        ciphertext_bytes[i] = int_to_bytes(ciphertext[i], byte_length)
    
    # 将字节数组合并
    ciphertext_bytes = b''.join(ciphertext_bytes)

    # 对字节进行base64编码
    ciphertext_str = byte2str_base64(ciphertext_bytes)

    return ciphertext_str

def RSA_Decrypt(ciphertext_str,private_key,modulus):
    byte_length = 8
    # 对base64进行解码
    ciphertext_bytes = str2byte_base64(ciphertext_str)

    # 对字节进行分组
    ciphertext_bytes = split_bytes(ciphertext_bytes, byte_length)

    length = len(ciphertext_bytes)

    # 将字节变为数字
    ciphertext_int = list(range(length))
    for i in range(length):
        ciphertext_int[i] = bytes_to_int(ciphertext_bytes[i])

    # 进行解密
    plaintext = list(range(length))
    for i in range(length):
        plaintext[i] = FastExpMod(ciphertext_int[i],private_key,modulus)
    
    # 进行解码
    for i in range(length):
        plaintext[i] = int_to_bytes(plaintext[i], byte_length)
        plaintext[i] = plaintext[i].lstrip(b'\x00')

    plaintext = b''.join(plaintext)

    plaintext = plaintext.decode('utf-8')

    return plaintext