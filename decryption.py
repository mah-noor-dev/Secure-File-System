# decryption.py
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Protocol.KDF import scrypt
import os
from pathlib import Path

class FileDecryptor:
    def decrypt_file(self, encrypted_path, password, output_dir="decrypted_files"):
        """
        Decrypts a file and saves it to the specified output_dir (default: "decrypted_files").
        """
        try:
            # Create output directory if it doesn't exist
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            # Read encrypted file (salt + IV + ciphertext)
            with open(encrypted_path, 'rb') as f:
                salt = f.read(16)
                iv = f.read(16)
                ciphertext = f.read()

            # Derive key using scrypt
            key = scrypt(
                password.encode(),
                salt,
                key_len=32,
                N=2**17,
                r=8,
                p=1
            )

            # Decrypt the data
            cipher = AES.new(key, AES.MODE_CBC, iv)
            plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

            # Generate output filename (remove "enc_" and ".bin")
            encrypted_filename = os.path.basename(encrypted_path)
            original_name = encrypted_filename.replace("enc_", "").replace(".bin", "")
            output_path = output_dir / original_name

            # Save decrypted file
            with open(output_path, 'wb') as f:
                f.write(plaintext)

            return str(output_path)

        except Exception as e:
            if "Padding is incorrect" in str(e):
                raise ValueError("Incorrect password or corrupted file")
            raise IOError(f"Decryption failed: {str(e)}")