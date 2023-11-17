from Crypto.Cipher import AES
import os
from math import log2
from collections import Counter

def calculate_entropy(data):
    if not data:
        return 0
    entropy = 0
    length = len(data)
    for count in Counter(data).values():
        frequency = count / length
        entropy -= frequency * log2(frequency)
    return entropy

def brute_force_aes_key(ciphertext, iv, known_key_bits=16, entropy_threshold=5.0):
    for i in range(2**known_key_bits):
        key = (i.to_bytes(2, byteorder='big') + b'\x00' * 14)
        try:
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted_aes = cipher.decrypt(ciphertext)
            if calculate_entropy(decrypted_aes) < entropy_threshold:
                # Save the decrypted data to a file for further processing
                with open('enc_1.hex', 'wb') as f:
                    f.write(decrypted_aes)
                return key
        except ValueError:
            continue
    return None

def read_encrypted_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

file_path = 'enc_2.hex'
ciphertext = read_encrypted_file(file_path)
iv = ciphertext[:16]
correct_key = brute_force_aes_key(ciphertext, iv)

if correct_key:
    with open('aes.key', 'wb') as file:
        file.write(correct_key)
    print(f"Key found and saved in aes.key: {correct_key.hex()}")
else:
    print("Key not found.")
