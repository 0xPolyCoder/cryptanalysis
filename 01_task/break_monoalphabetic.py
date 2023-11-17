import re
from ngram_score import NGramScore
from random import randint
import magic

# Function to perform frequency analysis on the ciphertext
def frequency_analysis(ciphertext):
    freq = {}
    for letter in ciphertext:
        if letter.isalpha():
            freq[letter] = freq.get(letter, 0) + 1
    freq_list = sorted(freq, key=freq.get, reverse=True)
    english_freq = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
    return dict(zip(freq_list, english_freq))

# Function to decrypt using the key
def decrypt(ciphertext, key):
    key_map = {v: k for k, v in key.items()}
    return ''.join(key_map.get(c, c) for c in ciphertext)

# Function to randomly transpose two letters in the key
def transpose_key(key):
    key = key.copy()
    idx1, idx2 = randint(0, 25), randint(0, 25)
    key_values = list(key.values())
    key_values[idx1], key_values[idx2] = key_values[idx2], key_values[idx1]
    return dict(zip(key.keys(), key_values))

# Load ciphertext
with open('enc_1.hex', 'rb') as file:
    ciphertext = file.read().decode('latin-1')

# Perform frequency analysis on the ciphertext
init_key = frequency_analysis(ciphertext)
ngram = NGramScore('english_quadgrams.txt')

# Hill-Climbing Algorithm
best_key = init_key
best_score = ngram.score(decrypt(ciphertext, best_key))
improved = True

while improved:
    improved = False
    for _ in range(1000):  # Number of iterations per step
        new_key = transpose_key(best_key)
        new_score = ngram.score(decrypt(ciphertext, new_key))
        if new_score > best_score:
            best_key = new_key
            best_score = new_score
            improved = True

# Decrypt the entire file content
decrypted_content = decrypt(ciphertext, best_key)

# Save the decrypted content to a file
with open('decrypted.txt', 'w') as file:
    file.write(decrypted_content)

# save the key
key_string = ''.join(best_key[chr(i)] for i in range(65, 91))  # ASCII values for A-Z
with open('monoalphabetic.key', 'w') as file:
    file.write(key_string)


print("Decryption complete. Content saved in decrypted.txt.")
