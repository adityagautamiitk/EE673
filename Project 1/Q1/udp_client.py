import socket

# Server Configuration (Must match the server script)
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12000

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Get user input
message = input("Input lowercase sentence: ")

# Send message to server
# UDP requires specifying the destination address with every send
client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

# Receive response from server
modified_message, server_address = client_socket.recvfrom(2048)

# Display the result
print("Reply from Server:", modified_message.decode())

client_socket.close()