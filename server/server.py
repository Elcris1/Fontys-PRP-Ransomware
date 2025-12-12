import asyncio
import websockets
from Connection import Connection, ConnectionState

class WebSocketCLIServer:
    def __init__(self, host="localhost", port=8765):
        self.host = host
        self.port = port
        self.connected_clients: dict[str, Connection] = {}  # Map username -> Connection
        self.__server = None
        self.__should_cli_run = True
        self.__selected_client: Connection = None

    async def handler(self, websocket):
        # websocket = connection
        """Handle incoming client connections and messages."""
        # First message must be an identifier (username)
        try:
            first_message = await websocket.recv()
            username = self.__check_first_message(first_message)

            if username is None:
                await websocket.send("Invalid initial message. Connection closing.")
                await websocket.close()
                return
            
            connection = Connection(uri=websocket.remote_address, socket=websocket)
            connection.set_username(username)
            connection.change_state(ConnectionState.IDENTIFIED)

            self.connected_clients[username] = connection
            print(f"[Connected] {username} joined")

            await websocket.send(f"Welcome, {username}!")

            async for message in websocket:
                print(f"[{username}] {message}")
                await self.broadcast(f"[{username}] {message}", sender=websocket)

        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            if websocket in self.connected_clients.values():
                print(f"[Disconnected] {self.connected_clients[websocket]} left")
                del self.connected_clients[websocket]

    def __check_first_message(self, message) -> str:
        """Check if the first message is a valid username."""
        if message.startswith("USERNAME:"):
            return message.split(":", 1)[1].strip()
        return None
    async def __cli(self):
        """Handle CLI input from the server terminal."""
        loop = asyncio.get_event_loop()
        while self.__should_cli_run:
            msg = await loop.run_in_executor(None, input, "CLI> ")
            if msg.lower() == "quit":
                print("Shutting down server...")
                await self.close_all_clients()
                self.__server.close()
                self.__should_cli_run = False
            print(f"[Server CLI] {msg}")
            #await self.broadcast(f"[Server CLI] {msg}")

    async def broadcast(self, message, sender=None):
        """Send a message to all connected clients."""
        for client in list(self.connected_clients.values()):
            if client != sender:  # Don't echo back to sender if desired
                try:
                    await client.send(message)
                except websockets.exceptions.ConnectionClosed:
                    del self.connected_clients[client]

    async def close_all_clients(self):
        """Close all client connections."""
        for websocket in list(self.connected_clients.values()):
            await websocket.close()

    async def __start_server(self):
        self.__server = await websockets.serve(
            self.handler,
            host = self.host,
            port = self.port,
            subprotocols=["json"]
        )
        await self.__server.wait_closed()

    async def start(self):
        """Start the WebSocket server and CLI loop."""
        print(f"WebSocket server running at ws://{self.host}:{self.port}")
        await asyncio.gather(self.__cli(), self.__start_server())


if __name__ == "__main__":
    server = WebSocketCLIServer()
    asyncio.run(server.start())
