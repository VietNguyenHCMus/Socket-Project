from fileinput import filename
import os
import socket

# Tạo một socket của client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Kết nối đến server qua địa chỉ và cổng
server_address = ('localhost', 8889)
client_socket.connect(server_address)

choice = input("Có gửi kèm file(1. Có, 2. Không): ")
if choice == 1:
    number_file = input("Số lượng file muốn gửi: ")
    
    while (number_file > 0):

        filename = input("Cho biết đường dẫn file thứ " + number_file + ": ")

        file = open(filename, "rb")
        file_size = os.path.getsize(filename)

        client_socket.send((filename).encode())
        client_socket.send(str(file_size).endcode())

        data = file.read()
        client_socket.sendall(data)
        client_socket.send(b"<END>")

        file.close()

client_socket.close()