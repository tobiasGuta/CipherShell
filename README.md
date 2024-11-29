# CipherShell

## Overview
SecureExec is a secure client-server communication tool that allows remote command execution over an encrypted SSL connection. This tool is designed to provide a secure channel for running commands on a target machine and receiving output remotely. The server can send commands, and the client will execute them and return the results.

---

## Features

- **SSL Encryption**: All communication between the client and server is encrypted with SSL to ensure secure data transmission.
- **Remote Command Execution**: The server sends commands to the client, which executes them and returns the output.
- **Cross-Platform**: Works on systems supporting Python and SSL (Linux, macOS, Windows).
- **Multithreading**: The server can handle multiple client connections simultaneously.
- **Command Output Handling**: Captures and sends back the output (or errors) from executed commands.

---

## Requirements

- Python 3.x
- `ssl` module (built-in with Python)
- `socket` module (built-in with Python)
- (Optional) Server-side SSL certificate (`server.crt`, `server.key`)

---

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/tobiasGuta/CipherShell.git
    cd CipherShell
    ```

2. Install dependencies (if any are required in the future):

    ```bash
    pip install -r requirements.txt
    ```

---

## Usage

### Starting the Server

To start the server, run the `server.py` file. The server listens for incoming client connections and allows you to send commands.

Input the server port when prompted.
The server will wait for client connections.

```bash
python server.py
```
### Starting the Client

To start the client, run the client.py file. The client connects to the server and executes commands.

```bash
python client.py
```

Input the server's IP address and port when prompted.
The client will receive commands from the server and send back the execution output.

### Security
SSL Encryption: All communication between the server and client is encrypted using SSL, ensuring secure data transmission.
Custom SSL Certificates: You can provide your own SSL certificates by replacing server.crt and server.key for enhanced security in production.
