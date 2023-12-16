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
            
            attachment_path = input(temp) 
            filename = os.path.basename(attachment_path)
           
            
            # Check content-type
            content_type = filename[-3:]
            temp = b''
            if(content_type == 'txt'): temp = 'application/octet-stream'
            if(content_type == 'pdf'): temp = 'application/pdf'
            if(content_type == 'ocx'): temp = 'application/msword'
            if(content_type == 'jpg'): temp = 'image/jpeg'
            if(content_type == 'png'): temp = 'image/png'
            if(content_type == 'zip'): temp = 'application/zip'
                
            client_socket.send(b'--<END>\r\n')
            client_socket.send(f'Content-Type: {temp}; name="{filename}"\r\n'.encode(FORMAT))
            client_socket.send(f'Content-Disposition: attachment; filename="{filename}"\r\n'.encode(FORMAT))
            client_socket.send(f'Content-Transfer-Encoding: base64\r\n\r\n'.encode(FORMAT))
            
            # Data transfer
            with open(filename, "rb") as f:
                data = f.read()
        
            data = base64.b64encode(data).decode(FORMAT)
            client_socket.sendall(data.encode(FORMAT) + b'\r\n')