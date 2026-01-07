# Overview
This is a ransomware simulation tool made for educational purposes as part of a university research project. It ilustrates how ransomware typically behaves so that defenders can have a better understanding on how to prevent and respond to ransomware attacks.

## Disclaimer (Important)
**This project is for EDUCATIONAL AND RESEARCH PURPOSES ONLY.**

- I do not condone or support malicious activity.

- Do not use this software on systems you do not own or do not have explicit permission to test.

- Any misuse of this project is solely the responsibility of the user.

Unauthorized deployment of ransomware or ransomware-like software may be illegal in your jurisdiction.

## License
This project is licensed under the MIT License - see the [MIT LICENSE](LICENSE) file for details.

## How to run
Create .env copying it from the example, this is required to modify any configuration outside from the [default configuration](.env.example)
### Copy file
````
cp .env.example .env
````
### Create a python environment
- Linux
```
python3 -m venv .venv
```
- Windows
````
py -m venv .venv
````
### Activate the environment
- Linux
````
source .venv/bin/activate
````
- Windows
````
.venv/Scripts/activate
````
### Install the libraries
- Linux/Windows
````
pip3 install -r requirements.txt
````
### Execution on auto/manual mode
- Linux
````
python3 main.py
````
- Windows
`````
py main.py
`````

### Execution on c2 mode
For this mode at least two terminals are required, one to run the server and the other one to run the main.py. The mode in the main module can be changed using the changeMode command or change in the .env file.
- Terminal 1
````
# Linux
python3 server/server.py

# Windows
py server/server.py
````
- Terminal 2
````
# Linux
python3 main.py

# Windows
py main.py
````



