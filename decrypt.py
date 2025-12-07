
if __name__ == "__main__":
    # key = load_key()
    # fernet = Fernet(key)
    # decrypt_file("mock files/a.txt", "mock files/a.txt", fernet)
    import os
    import platform 
    from main import Program
    import json

    system = platform.system()
    base = os.path.dirname(os.path.realpath(__file__))

    # since windows does not support syslink we need to change the working directory
    if system == "Windows":
        cwd = os.getcwd()
        #added_line_script
        os.chdir(cwd)
        base = cwd

    path = os.path.join(base, "discovered_info.json")

    with open(path, "r") as conf_file:
        data = json.load(conf_file)
        print(data)


    program = Program(data=data, mode="auto", system=platform.system())
    program.load_key()
    program.decrypt()
    program.delete_traces()
