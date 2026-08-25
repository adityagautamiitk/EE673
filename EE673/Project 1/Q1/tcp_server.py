import socket

# Server Configuration
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12001      # Using a different port to avoid conflict

# Create a TCP socket
# SOCK_STREAM indicates TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket
server_socket.bind((SERVER_IP, SERVER_PORT))

# Listen for incoming connections (queue up to 1 request)
server_socket.listen(1)

print(f"TCP Server is ready to receive on {SERVER_IP}:{SERVER_PORT}...")

while True:
    # accept() blocks until a client connects
    # It returns a new socket object (connection_socket) specific to this client
    connection_socket, addr = server_socket.accept()
    print(f"Connection established with {addr}")
    
    # Receive data (buffer size 1024)
    message = connection_socket.recv(1024)
    
    # Process data
    modified_message = message.decode().upper()
    
    # Send back using the dedicated connection socket
    connection_socket.send(modified_message.encode())
    
    # Close the connection with this specific client
    connection_socket.close()