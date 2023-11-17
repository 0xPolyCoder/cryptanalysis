def xor_bytes(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

def dec(ciphertext, key): # will do the same as xor_byes, created this funtion just for clarity view
    return xor_bytes(ciphertext, key) 

def main():
    with open('task02.cryp', 'rb') as file:
        c = file.read()

    with open('sentence_1.txt', 'rb') as file:
        p1 = file.read()

    with open('sentence_2.txt', 'rb') as file:
        p2 = file.read()

    k1 = xor_bytes(c, p1)
    k2 = xor_bytes(c, p2)

    print('ciphertext: ')
    print(c)
    print("================================================")

    print('k1: ')
    print(k1)
    print("================================================")

    print('k2: ')
    print(k2)
    print("================================================")

    print('dec(c, k1): ')
    print(dec(c, k1))
    print("================================================")

    print('dec(c, k2): ')
    print(dec(c, k2))
    print("================================================")

    if dec(c, k1) == p1 and dec(c, k2) == p2:
        print("the solution is correct")

    # Save k1 and k2 to binary files
    with open('sentence_1.key', 'wb') as file:
        file.write(k1)
    with open('sentence_2.key', 'wb') as file:
        file.write(k2)

if __name__ == "__main__":
    main()

