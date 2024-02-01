import tkinter as tk
from tkinter import ttk
import AES
import time

def encrypt_message():
    message = entry_message.get()
    start_time = time.time()

    Ciphertext,Key_string = AES.AES_Encode(message)

    end_time = time.time()
    elapsed_time = end_time-start_time

    text_result_encryption.delete(1.0, "end")  # 清空文本框
    text_result_encryption.insert(1.0, Ciphertext)  # 显示加密结果

    text_generate_key.delete(1.0,"end")
    text_generate_key.insert(1.0, Key_string)

    label_encrypt_time.config(text=f"加密时间为： {elapsed_time:.6f} 秒")

def decrypt_message():
    Ciphertext = entry_cipher.get()
    Key = entry_decryption_key.get()
    start_time = time.time()

    Texts = AES.AES_Decode(Ciphertext, Key)

    end_time = time.time()
    elapsed_time = end_time-start_time

    text_result_decryption.delete(1.0, "end")  # 清空文本框
    text_result_decryption.insert(1.0, Texts)  # 显示解密结果

    label_decrypt_time.config(text=f"解密时间为： {elapsed_time:.6f} 秒")


root = tk.Tk()
root.title("AES 加密解密模拟")
# 加密窗口
frame_encryption = ttk.LabelFrame(root, text="加密窗口")
frame_encryption.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

label_message = ttk.Label(frame_encryption, text="消息:")
label_message.grid(row=0, column=0, padx=5, pady=5)
entry_message = ttk.Entry(frame_encryption)
entry_message.grid(row=0, column=1, padx=5, pady=5)

button_encrypt = ttk.Button(frame_encryption, text="加密消息", command=encrypt_message)
button_encrypt.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

label_result_encryption = ttk.Label(frame_encryption, text="加密结果:")
label_result_encryption.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

text_result_encryption = tk.Text(frame_encryption, height=5, width=40)
text_result_encryption.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

label_generate_key = ttk.Label(frame_encryption, text="生成的密钥：")
label_generate_key.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

text_generate_key = tk.Text(frame_encryption, height=5, width=40)
text_generate_key.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

label_encrypt_time = ttk.Label(frame_encryption, text="加密时间为：")
label_encrypt_time.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
# 解密窗口
frame_decryption = ttk.LabelFrame(root, text="解密窗口")
frame_decryption.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

label_cipher = ttk.Label(frame_decryption, text="密文:")
label_cipher.grid(row=0, column=0, padx=5, pady=5)
entry_cipher = ttk.Entry(frame_decryption)
entry_cipher.grid(row=0, column=1, padx=5, pady=5)

label_decryption_key = ttk.Label(frame_decryption, text="密钥:")
label_decryption_key.grid(row=1, column=0, padx=5, pady=5)
entry_decryption_key = ttk.Entry(frame_decryption)
entry_decryption_key.grid(row=1, column=1, padx=5, pady=5)

button_decrypt = ttk.Button(frame_decryption, text="解密消息", command=decrypt_message)
button_decrypt.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

label_result_decryption = ttk.Label(frame_decryption, text="解密结果：")
label_result_decryption.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

text_result_decryption = tk.Text(frame_decryption, height=5, width=40)
text_result_decryption.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

label_decrypt_time = ttk.Label(frame_decryption, text="解密时间为：")
label_decrypt_time.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()