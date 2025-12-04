from cryptography.fernet import Fernet


def encrypt_file(filename, fernet: Fernet, encryption: bool = True):
    print(f"Encrypting {filename}")
    if not encryption:
        return
    
    with open(filename, "rb") as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    with open(filename + ".enc", "wb") as encrypted_file:
        encrypted_file.write(encrypted)

    print(f"{filename} has been encrypted.")


if __name__ == "__main__":
    # Generate a key
    key = Fernet.generate_key()

    # Save the key to a file
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

    print("Encryption key saved as secret.key")
    fernet = Fernet(key)

    encrypt_file("mock files/a.txt", fernet)
