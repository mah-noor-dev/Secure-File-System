# encryption.py
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt
import os

class FileEncryptor:
    def encrypt_file(self, file_path, password):
        # Generate salt and derive key
        salt = get_random_bytes(16)
        key = scrypt(password.encode(), salt, key_len=32, N=2**17, r=8, p=1)
        
        # Generate IV and create cipher
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Read and encrypt file
        with open(file_path, 'rb') as f:
            plaintext = f.read()
        
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
        
        # Save encrypted file
        encrypted_filename = f"enc_{os.path.basename(file_path)}.bin"
        encrypted_path = os.path.join('encrypted_files', encrypted_filename)
        
        with open(encrypted_path, 'wb') as f:
            f.write(salt)
            f.write(iv)
            f.write(ciphertext)
        
        # Save key info (in real system, you'd encrypt this)
        key_filename = f"key_{os.path.basename(file_path)}.bin"
        key_path = os.path.join('keys', key_filename)
        
        with open(key_path, 'wb') as f:
            f.write(key)
        
        return encrypted_path, key_path