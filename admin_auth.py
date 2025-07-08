import os
import json
import getpass
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
import base64

class AdminAuth:
    def __init__(self):
        if not os.path.exists('config.json'):
            with open('config.json', 'w') as f:
                json.dump({
                    "admin_hash": "",
                    "salt": base64.b64encode(get_random_bytes(16)).decode(),
                    "iterations": 131072  # Changed to power of 2
                }, f)
    
    def is_admin_configured(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
        return bool(config.get('admin_hash'))
    
    def setup_admin(self):
        print("\nAdmin Account Setup")
        password = getpass.getpass("Enter admin password: ")
        confirm = getpass.getpass("Confirm admin password: ")
        
        if password != confirm:
            print("Passwords don't match!")
            return False
            
        with open('config.json', 'r+') as f:
            config = json.load(f)
            salt = base64.b64decode(config['salt'].encode())
            admin_hash = scrypt(
                password.encode(),
                salt,
                key_len=64,
                N=131072,  # Fixed value
                r=8,
                p=1
            )
            config['admin_hash'] = base64.b64encode(admin_hash).decode()
            f.seek(0)
            json.dump(config, f)
            f.truncate()
        
        print("Admin account created successfully!")
        return True
    
    def authenticate_admin(self):
        if not self.is_admin_configured():
            print("No admin account configured!")
            return False
            
        password = getpass.getpass("Enter admin password: ")
        
        with open('config.json', 'r') as f:
            config = json.load(f)
            salt = base64.b64decode(config['salt'].encode())
            stored_hash = base64.b64decode(config['admin_hash'].encode())
            
            input_hash = scrypt(
                password.encode(),
                salt,
                key_len=64,
                N=131072,  # Fixed value
                r=8,
                p=1
            )
            
            return input_hash == stored_hash