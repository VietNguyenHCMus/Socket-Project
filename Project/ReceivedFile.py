import socket

FORMAT = "uft-8"
SIZE = 1024

def receivedFile(client_socket):
    
    # Receiving filename and filesize from sendFile func           
    data = client_socket.recv(SIZE).decode(FORMAT)
    item = data.split("_")
    filename = item[0]
    filesize = int(item[1])
    client_socket.send("Filename and filesize received".encode(FORMAT))
    
    # Data transfer
    
    with open(f"recv_{filename}", "wb") as f:
        data = client_socket.recv(SIZE)
        
        while data:
            f.write(data)
            data = client_socket.recv(SIZE)

