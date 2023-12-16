import os
import socket
import base64

FORMAT = "utf8"
SIZE = 1024

def sendFile(client_socket):

    choice = int(input("Có gửi kèm file(1. Có, 2. Không): "))
    if choice == 1:
        number_file = int(input("Số lượng file muốn gửi: "))
        ordinal_number = 1
        while (number_file > 0):
            
            number_file -= 1
            
            temp = "Cho biết đường dẫn thứ {}".format(ordinal_number) + ": "
            ordinal_number += 1
            
            filename = input(temp) 
            
            # Sending filename and filesize to server
            data = f"{filename}"
            client_socket.send(data.encode())
            
            # Data transfer
            with open(filename, "rb") as f:
                data = f.read()
        
            data = base64.b64encode(data).decode(FORMAT)
            client_socket.sendall(data.encode(FORMAT))