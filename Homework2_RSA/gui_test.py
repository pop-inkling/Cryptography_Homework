import tkinter as tk
from tkinter import ttk
import time
from prime_num import create_keys
from RSA import RSA_Encrypt, RSA_Decrypt

text = '我想测试一下RSA的性能'
modulus,public_key,private_key = create_keys(8)

def encrypt_message():
    message = entry_message.get()
    public_key = entry_public_key.get()
    modulus = entry_modulus_send.get()
    start_time = time.perf_counter()

    Ciphertext = RSA_Encrypt(message,int(public_key),int(modulus))

    end_time = time.perf_counter()
    elapsed_time = end_time-start_time

    text_result_encryption.delete(1.0, "end")  # 清空文本框
    text_result_encryption.insert(1.0, Ciphertext)  # 显示加密结果

    label_encrypt_time.config(text=f"加密时间为：{elapsed_time:.6f} 秒")

def decrypt_message():
    Ciphertext = entry_cipher.get()
    private_key = entry_private_key.get()
    modulus = entry_modulus_rec.get()
    start_time = time.perf_counter()


    Texts = RSA_Decrypt(Ciphertext,int(private_key),int(modulus))

    end_time = time.perf_counter()

    elapsed_time = end_time-start_time

    text_result_decryption.delete(1.0, "end")  # 清空文本框
    text_result_decryption.insert(1.0, Texts)  # 显示解密结果

    label_decrypt_time.config(text=f"解密时间为： {elapsed_time:.6f} 秒")


root = tk.Tk()
root.title("RSA 加密解密模拟")

# 密钥窗口
frame_keys = ttk.LabelFrame(root,text="生成的密钥")
frame_keys.grid(row=0, column=0,columnspan=2, padx=10, pady=10)

text_widget = tk.Text(frame_keys, wrap='word', height=15, width=50)
text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

text_widget.insert(tk.END, "私钥:\n" + str(private_key) + "\n\n")
text_widget.insert(tk.END, "公钥:\n" + str(public_key)+ "\n\n")
text_widget.insert(tk.END, "公开模数:\n" + str(modulus))

text_widget.config(state=tk.DISABLED)

# 加密窗口
frame_encryption = ttk.LabelFrame(root, text="加密窗口")
frame_encryption.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

label_message = ttk.Label(frame_encryption, text="消息:")
label_message.grid(row=0, column=0, padx=5, pady=5)
entry_message = ttk.Entry(frame_encryption)
entry_message.grid(row=0, column=1, padx=5, pady=5)

label_public_key = ttk.Label(frame_encryption, text="对方的公钥:")
label_public_key.grid(row=1, column=0, padx=5, pady=5)
entry_public_key = ttk.Entry(frame_encryption)
entry_public_key.grid(row=1, column=1, padx=5, pady=5)

label_modulus_send = ttk.Label(frame_encryption, text="对方的公开模数:")
label_modulus_send.grid(row=2, column=0, padx=5, pady=5)
entry_modulus_send = ttk.Entry(frame_encryption)
entry_modulus_send.grid(row=2, column=1, padx=5, pady=5)

button_encrypt = ttk.Button(frame_encryption, text="加密消息", command=encrypt_message)
button_encrypt.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

label_result_encryption = ttk.Label(frame_encryption, text="加密结果:")
label_result_encryption.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

text_result_encryption = tk.Text(frame_encryption, height=5, width=40)
text_result_encryption.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

label_encrypt_time = ttk.Label(frame_encryption, text="加密时间为：")
label_encrypt_time.grid(row=6, column=0, columnspan=2, padx=5, pady=5)


# 解密窗口
frame_decryption = ttk.LabelFrame(root, text="解密窗口")
frame_decryption.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

label_cipher = ttk.Label(frame_decryption, text="密文:")
label_cipher.grid(row=0, column=0, padx=5, pady=5)
entry_cipher = ttk.Entry(frame_decryption)
entry_cipher.grid(row=0, column=1, padx=5, pady=5)

label_private_key = ttk.Label(frame_decryption, text="己方的私钥:")
label_private_key.grid(row=1, column=0, padx=5, pady=5)
entry_private_key = ttk.Entry(frame_decryption)
entry_private_key.grid(row=1, column=1, padx=5, pady=5)

label_modulus_rec = ttk.Label(frame_decryption, text="己方的公开模数:")
label_modulus_rec.grid(row=2, column=0, padx=5, pady=5)
entry_modulus_rec = ttk.Entry(frame_decryption)
entry_modulus_rec.grid(row=2, column=1, padx=5, pady=5)

button_decrypt = ttk.Button(frame_decryption, text="解密消息", command=decrypt_message)
button_decrypt.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

label_result_decryption = ttk.Label(frame_decryption, text="解密结果：")
label_result_decryption.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

text_result_decryption = tk.Text(frame_decryption, height=5, width=40)
text_result_decryption.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

label_decrypt_time = ttk.Label(frame_decryption, text="解密时间为：")
label_decrypt_time.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()