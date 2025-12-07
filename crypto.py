from cryptography.fernet import Fernet
import os

class CryptoGraphy:
    def __init__(self, fernet: Fernet = None, should_encrypt: bool = True, should_delete_original: bool = True):
        self.__fernet__ = fernet
        self.__should_encrypt__ = should_encrypt
        self.__should_delete_original__ = should_delete_original
    
    def encrypt(self, filename: str):
        print(f"Encrypting {filename}")

        if not self.__should_encrypt__:
            return
        
        with open(filename, "rb") as file:
            original = file.read()

        encrypted = self.__fernet__.encrypt(original)

        with open(filename + ".ENCRYPTED", "wb") as encrypted_file:
            encrypted_file.write(encrypted)

        if self.__should_delete_original__:
            os.remove(filename)

        print(f"{filename} has been encrypted.")

    def decrypt(self, encrypted_filename: str):
        print(f"Decrypting {encrypted_filename}")
        if not self.__should_encrypt__:
            return
        
        with open(encrypted_filename, "rb") as enc_file:
            encrypted = enc_file.read()

        decrypted = self.__fernet__.decrypt(encrypted)
        output_filename = encrypted_filename.split(".ENCRYPTED")[0]

        with open(output_filename, "wb") as dec_file:
            dec_file.write(decrypted)

        if self.__should_delete_original__:
            os.remove(encrypted_filename)

        print(f"{encrypted_filename} has been decrypted to {output_filename}.")

    def setup(self, key_filename: str = "secret.key"):
        key = Fernet.generate_key()

        with open(key_filename, "wb") as key_file:
            key_file.write(key)

        print(f"Encryption key saved as {key_filename}")
        self.__fernet__ = Fernet(key)

    def load_key(self, key_filename: str = "secret.key"):
        with open(key_filename, "rb") as key_file:
            key = key_file.read()
            
        self.__fernet__ = Fernet(key)
        return key