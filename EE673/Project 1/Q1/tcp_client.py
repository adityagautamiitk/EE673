import socket

# Server Configuration
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12001

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server (This performs the 3-way handshake)
client_socket.connect((SERVER_IP, SERVER_PORT))

# Get user input
message = input("Input lowercase sentence: ")

# Send the message
client_socket.send(message.encode())

# Receive the response
modified_message = client_socket.recv(1024)

# Print result
print("Reply from Server:", modified_message.decode())

# Close the connection
client_socket.close()