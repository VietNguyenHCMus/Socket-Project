import os
import socket

# Tạo một socket của client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Kết nối đến server qua địa chỉ và cổng
server_address = ('localhost', 8889)
client_socket.connect(server_address)

file = open("filename", "rb")
file_size = os.path.getsize("filename")

client_socket.send("received_file".encode())
client_socket.send(str(file_size).endcode())

data = file.read()
client_socket.sendall(data)
client_socket.send(b"<END>")

file.close()
client_socket.close()