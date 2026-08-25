import socket

# Server Configuration
SERVER_IP = '127.0.0.1'  # Localhost
SERVER_PORT = 12000      # Arbitrary non-privileged port

# Create a UDP socket
# AF_INET indicates IPv4, SOCK_DGRAM indicates UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the IP and Port
server_socket.bind((SERVER_IP, SERVER_PORT))

print(f"UDP Server is up and listening on {SERVER_IP}:{SERVER_PORT}...")

while True:
    # recvfrom receives data and the address of the sender
    # Buffer size is 2048 bytes
    message, client_address = server_socket.recvfrom(2048)
    
    print(f"Received connection from {client_address}")
    
    # Decode raw bytes to string and convert to uppercase
    modified_message = message.decode().upper()
    
    # Send the modified message back to the client using the sender's address
    server_socket.sendto(modified_message.encode(), client_address)