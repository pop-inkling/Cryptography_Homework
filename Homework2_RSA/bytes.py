import base64

def split_bytes(data, chunk_size):
    """ 将字节数据分割成指定大小的块。 """
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

def bytes_to_int(bytes_data):
    """将字节序列转换为整数"""
    return int.from_bytes(bytes_data, byteorder='big')

# 每六个字节进行分割，保证最后得到的大数要小于模数
def str2array_Plain(text):
    # 将字符串转换为字节序列
    text_bytes = text.encode('utf-8')
    # 按每6字节分割
    chunks = split_bytes(text_bytes, 6)

    byte_arrays = [list(chunk) for chunk in chunks]

    # 补全最后一个数组（如果不足6字节）
    if len(byte_arrays[-1]) < 6:
        byte_arrays[-1].extend([0] * (6 - len(byte_arrays[-1])))
    
    plaintext_int = list(range(len(byte_arrays)))
    for i in range(len(byte_arrays)):
        plaintext_int[i] = bytes_to_int(byte_arrays[i])
    
    return plaintext_int

# 将大整数转换为字节序列
def int_to_bytes(integer, length):
    """将整数转换为字节序列"""
    return integer.to_bytes(length, byteorder='big')

def byte2str_base64(combined_bytes):
    array_string = base64.b64encode(combined_bytes)
    array_string = array_string.decode('ascii')

    return array_string

def str2byte_base64(string):
    bytes = string.encode('ascii')
    bytes = base64.b64decode(bytes)

    return bytes