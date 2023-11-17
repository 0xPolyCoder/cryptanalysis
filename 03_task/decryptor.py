import sys

def xor_data(data, key):
    key_len = len(key)
    return bytes(data[i] ^ key[i % key_len] for i in range(len(data)))

def read_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

def write_file(content, file_path):
    with open(file_path, 'wb') as file:
        file.write(content)

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 decryptor.py [encrypted file] [key in hex] [output file]")
        sys.exit(1)

    encrypted_file = sys.argv[1]
    key_hex = sys.argv[2]
    output_file = sys.argv[3]

    try:
        key = bytes.fromhex(key_hex)
    except ValueError:
        print("Invalid key format. Key must be in hexadecimal.")
        sys.exit(1)

    encrypted_data = read_file(encrypted_file)
    decrypted_data = xor_data(encrypted_data, key)

    write_file(decrypted_data, output_file)
    print(f"Decrypted file written to {output_file}")

if __name__ == "__main__":
    main()
