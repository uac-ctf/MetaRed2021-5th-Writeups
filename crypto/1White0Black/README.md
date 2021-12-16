# Tribute
**AUTHOR**

botto

**CATEGORY**

crypto

**DIFFICULTY**

easy

**DESCRIPTION**
```
Aveiro is beautiful, but we challenge you to explore its hidden spots.
```

**SOLVE**
```
The provided image contains a .zip file inside. 

$ binwalk -e kasiski_aveiro.png 

This extracts the zip file. Then, use JohnTheRipper to crack the password.
$ zip2john file.zip > hash.txt
$ john --format=pkzip --wordllist=rockyou.txt hash.txt

Which outputs the password for the zip: "qwertyuiop"

Inside the zip there are 2 images: 0.png and 1.png. 

XOR the images and with the result of that operation rebuild a new image -> gives a QR code.

After reading the QR code, you are presented with a string of characters, proceed to do these operations:
	-> decode base64
	-> decode base32 from the result of the previous step
	-> decode hex from the result of the previous step
	-> decypher vigenere using key "aveiro" from the result of the previous step

The vigenere step is not random. The filename of the image is kasiski_aveiro.png, being kasiski method used to break vigenere cipher (thus inducting that vigenere is present) and aveiro being the key.
```

**FLAG**
```
CTFUA{Qr_c0d35_4r3_FuN}
```
