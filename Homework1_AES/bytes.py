import numpy as np
import base64
# 接受到字符串后进行转化
def split_bytes(data, chunk_size):
    """ 将字节数据分割成指定大小的块。 """
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

# 将字节进行分割
def str2array_Plain(text):
    # 将字符串转换为字节序列
    text_bytes = text.encode('utf-8')
    # 按每16字节分割
    chunks = split_bytes(text_bytes, 16)

    byte_arrays = [list(chunk) for chunk in chunks]

    # 补全最后一个数组（如果不足16字节）
    if len(byte_arrays[-1]) < 16:
        byte_arrays[-1].extend([0] * (16 - len(byte_arrays[-1])))

    byte_arrays = np.array(byte_arrays, dtype=int) #将list类型变为nparray类型，方便运算

    return byte_arrays

# 对Numpy数组base64编码为字符串
def array2str_base64(arrays):
    arrays = arrays.astype(np.uint8)
    array_bytes = arrays.tobytes()
    array_string = base64.b64encode(array_bytes)
    array_string = array_string.decode('ascii')

    return array_string

# 将字符串base64解码为Numpy数组
def str2array_base64(string):
    arrays = string.encode('ascii')
    arrays = base64.b64decode(arrays)
    arrays = list(arrays)
    arrays = np.array(arrays)

    return arrays

