import os
from zipfile import ZipFile, ZIP_DEFLATED
from io import BytesIO

def create_dummy_zip(target_size, temp_file):
    # Start with an estimate of the content size, then adjust as needed
    content_size = 1536300 #after multiple trials, this content size is the closest

    while True:
        dummy_content = BytesIO()
        with ZipFile(dummy_content, 'w', compression=ZIP_DEFLATED) as dummy_zip:
            dummy_zip.writestr('dummy.txt', '0' * content_size)
        print(dummy_content.tell())
        print(target_size)
        print(content_size)
        if dummy_content.tell() == target_size:
            break
        elif dummy_content.tell() > target_size:
            content_size -= 100
        else:
            content_size += 100

    # Write the final dummy content to a file
    with open(temp_file, 'wb') as file:
        file.write(dummy_content.getvalue())

def xor_files(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        return bytes(a ^ b for a, b in zip(f1.read(), f2.read()))

def main():
    encrypted_file = 'encrypted.zip.hex'
    dummy_file = 'dummy.zip'
    output_keys_file = 'possible_keys.txt'

    # Create a dummy zip file with the same size as the encrypted file
    encrypted_size = os.path.getsize(encrypted_file)
    create_dummy_zip(encrypted_size, dummy_file)

    # XOR the files and find possible keys
    xor_result = xor_files(encrypted_file, dummy_file)

    # Extracting keys
    possible_keys = [xor_result[i:i+10] for i in range(len(xor_result) - 9)]  # 10 bytes (80 bits) key

    # Write possible keys to a file
    with open(output_keys_file, 'w') as f:
        for key in possible_keys:
            f.write(key.hex() + '\n')

if __name__ == "__main__":
    main()
