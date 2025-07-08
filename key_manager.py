import os
from Crypto.Protocol.KDF import scrypt
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import json

class KeyManager:
    def __init__(self):
        self._load_config()
        
    def _load_config(self):
        with open('config.json', 'r') as f:
            self.config = json.load(f)
        
    def generate_aes_key(self):
        return get_random_bytes(32)  # 256-bit key
        
    def encrypt_aes_key(self, aes_key):
        # In a real system, this would use the admin's passphrase
        # For demo, we'll use a hardcoded key derivation salt
        salt = self.config['salt'].encode()
        admin_key = scrypt(
            password="admin_passphrase",  # Would be entered by admin in real system
            salt=salt,
            key_len=32,
            N=2**20,
            r=8,
            p=1
        )
        
        iv = get_random_bytes(16)
        cipher = AES.new(admin_key, AES.MODE_CBC, iv)
        padded_key = pad(aes_key, AES.block_size)
        encrypted_key = iv + cipher.encrypt(padded_key)
        
        return encrypted_key
        
    def decrypt_aes_key(self, encrypted_key):
        salt = self.config['salt'].encode()
        admin_key = scrypt(
            password="admin_passphrase",  # Would be entered by admin in real system
            salt=salt,
            key_len=32,
            N=2**20,
            r=8,
            p=1
        )
        
        iv = encrypted_key[:16]
        ciphertext = encrypted_key[16:]
        
        cipher = AES.new(admin_key, AES.MODE_CBC, iv)
        decrypted_key = unpad(cipher.decrypt(ciphertext), AES.block_size)
        
        return decrypted_key