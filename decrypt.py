
if __name__ == "__main__":
    # key = load_key()
    # fernet = Fernet(key)
    # decrypt_file("mock files/a.txt", "mock files/a.txt", fernet)
    import os
    import platform
    #added_line_script
    from main import Program
    import json

    BASE = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(BASE, "discovered_info.json")

    with open(path, "r") as conf_file:
        data = json.load(conf_file)
        print(data)


    program = Program(data=data, mode="auto", system=platform.system())
    program.load_key()
    program.decrypt()
    program.delete_traces()
