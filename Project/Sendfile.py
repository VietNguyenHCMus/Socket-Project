from fileinput import filename
import os
import socket

# Tạo một socket của client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Kết nối đến server qua địa chỉ và cổng
server_address = ('localhost', 2225)
client_socket.connect(server_address)

choice = int(input("Có gửi kèm file(1. Có, 2. Không): "))
if choice == 1:
    number_file = int(input("Số lượng file muốn gửi: "))
    
    while (number_file > 0):
        
        number_file -= 1

        file = open("input.txt", "rb")
        file_size = os.path.getsize("input.txt")

        client_socket.send(("newinput.txt").encode())
        client_socket.send(str(file_size).encode())

        data = file.read()
        client_socket.sendall(data)
        client_socket.send(b"<END>")

        file.close()

client_socket.close()