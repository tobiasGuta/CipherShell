import socket
import ssl
import threading

# Function to execute commands on the client and send output to the server
def handle_client(client_socket, addr):
    print(f"Connection established with {addr}")
    
    while True:
        # Receive the command from the server
        command = input("Enter command to send to client: ")  # Server sends command to client
        if command.lower() == "exit":
            print("Exiting...")
            break

        # Send the command to the client
        client_socket.send(command.encode())

        # Receive the output from the client
        output = client_socket.recv(1024).decode()
        print(f"Client response:\n{output}")

    client_socket.close()

# Start the server to listen for client connections
def start_server():
    host = '0.0.0.0'  # Server binds to all available network interfaces
    port = int(input("Enter the server port: "))

    # Create an unencrypted server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))  # Bind to all interfaces and user-specified port
    server_socket.listen(5)  # Listen for up to 5 connections

    # Create an SSL context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    # Wrap the server socket with SSL using the context
    server_socket = context.wrap_socket(server_socket, server_side=True)

    print(f"Server waiting for connections on port {port}...")
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

# Start the server
start_server()
