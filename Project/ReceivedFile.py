import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()

client, addr = server.accept()

file_name = client.recv(1024).decode()
print(file_name)
file_size = client.recv(1024).decode()
print(file_size)

file = open(file_name, "wb")

file_byte = b""

done = False

while not done:
    data = client.recv(1024)
    if file_byte[-5:] == b"<END>":
        done = True
    else:
        file_byte += data

file.write(file_byte)

file.close()
client.close()
server.close()

#hainam