import socket

FORMAT = "uft-8"
SIZE = 1024
localhost = '127.0.0.1'
# Tạo một socket của client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Kết nối đến server qua địa chỉ và cổng
server_address = (localhost, 3335)

def receivedFile(client_socket, server_address):
    
    client_socket.connect(server_address)
    conn = client_socket.accept()
    # Receiving filename and filesize from sendFile func           
    data = conn.recv(SIZE).decode(FORMAT)
    item = data.split("_")
    filename = item[0]
    filesize = int(item[1])
    conn.send("Filename and filesize received".encode(FORMAT))
    
    # Data transfer
    
    with open(f"recv_{filename}", "wb") as f:
        data = conn.recv(SIZE)
        
        while data:
            f.write(data)
            data = conn.recv(SIZE)
        conn.close()
        f.close()
        
    client_socket.close()
receivedFile(client_socket, server_address)
