First we know few things:
- The key is 80bit
- The encryption algoritm used is XOR
- The zip used a compression algorithm, version 3.20, which means it's ZIP_DEFLATED

To approach this, the easiest way came to my mind is to:


1. Make a script that would:
	1. Make a `dummy.zip` that will be compressed using the same algoritm, and will have exactly the same size as our encrypted file, we know that xor encryption does not change the file size.
		 - It's little tricky to make the a compressed file with the same size as our target file, that's why in the script there's a while true loop that will check `dummy.zip` size after compression, if it's bigger than our `encrypted.zip.hex`, it will decrease the content, if it's more it will decrease and will only stop if the size is the same.
	2. XOR our `dummy.zip` with `encrypted.zip.hex`, then the result must be a series of keys, split the whole thing into multiple keys of 10 bytes, then save it in a file with hex ascii encoding.
	3. Now that we have possible keys that are mostly partially correct especially the keys that will be in positions of the header, EOCD..etc
	4. Getting the first key(`6d5b8ff8ddfaadc12981`): we know for sure that at least the first 4 bytes are correct because of the magic number `PK\x03\x04`, so trying the first, gives almost full decryption, it shows the string `You have#successfuoly decrypwed the zis file :-)	PK?u`, this means that mostly the first key is correct, but only few bits in the rest 6 bytes are not correct.
	5. To complete our key, I check now the footer, in which there's probably the signature of EOCD end.
	6.  So I retrieved this key that seems closer to our first key and it's on the bottom closer to the end: `6d588f76ddfaad432a81`


After trying multiple combinations by taking the first key, and change only 4 bits at time from the second key, i finally got the correct key which is: `6d5b8ff8ddfaadc12981`
-  First key in the list: 
	- `6d 5b 8f f8 dd f9 ad c1 29 81`
-  4th key before last key in the list: 
	- `6d 58 8f 76 dd fa ad 43 2a 81`
- correct key after replacing 9 from first key with a in last key
	- `6d 5b 8f f8 dd fa ad c1 29 81`

To decrypt, I created a small command line tool in python that takes encrypted file, hex encoded key, output path

I decrypted the file and got the files: `ReadMe.md` and `RAW_Packet.c`.

The `ReadMe.md` contains:
  
Congratulations!
You have successfully decrypted the zip file :-)

