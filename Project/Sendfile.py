import os
import socket
import base64

FORMAT = "uft-8"
SIZE = 1024
# Tạo một socket của client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Kết nối đến server qua địa chỉ và cổng
server_address = ('localhost', 3335)


def sendFile(client_socket, server_address):

    client_socket.connect(server_address)

    choice = int(input("Có gửi kèm file(1. Có, 2. Không): "))
    if choice == 1:
        number_file = int(input("Số lượng file muốn gửi: "))
        ordinal_number = 1
        while (number_file > 0):
            
            number_file -= 1
            
            temp = "Cho biết đường dẫn thứ {}".format(ordinal_number) + ": "
            ordinal_number += 1
            
            filename = input(temp) 
            filesize = os.path.getsize(filename)
            
            # Sending filename and filesize to server
            data = f"{filename}_{filesize}"
            client_socket.send(data.encode())
            
            # Data transfer
            with open(filename, "rb") as f:
                data = f.read()
                while data:
                    client_socket.send(data)
                    data = f.read(SIZE)
                f.close()
                

    client_socket.close()
    

sendFile(client_socket, server_address)