# Portable password input
from getpass import getpass
from socket import *
import ssl
from Sendfile import sendFile

FORMAT = 'utf-8'

localhost = '127.0.0.1'

SenderEmail = input("Enter Your Email Address: ")
# SenderPassword = getpass("Enter Your Password: ")  # Commented out to remove password input
ReceiverEmail = input("Enter Email Destination: ")
Subject = input("Enter Email Subject: ")
EmailBody = input("Enter Email Body Message: ")

# Message included in body
msg = '{}. \r\n'.format(EmailBody)

# Choose a mail server (e.g., Google mail server) and call it mailserver
server_address = (localhost, 2225)

# Fill in start
# Creating socket called clientSocket
clientSocket = socket(AF_INET, SOCK_STREAM)

# Establishing a TCP connection with mailserver
clientSocket.connect(server_address)

confMsg = clientSocket.recv(1024)
print(confMsg)
if confMsg[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print serverresponse.
heloCommand = 'EHLO ' + localhost + '\r\n';
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send MAIL FROM command and print server response.
mailfrom = "MAIL FROM: <{}>\r\n".format(SenderEmail)
clientSocket.send(mailfrom.encode())
confMsg5 = clientSocket.recv(1024).decode()
print(confMsg5)

# Send RCPT TO command and print server response.
rcptto = "RCPT TO: <{}>\r\n".format(ReceiverEmail)
clientSocket.send(rcptto.encode())
confMsg6 = clientSocket.recv(1024).decode()


# Send DATA command and print server response.
data = 'DATA\r\n'
clientSocket.send(data.encode())
confMsg7 = clientSocket.recv(1024).decode()
print(confMsg7)

# Send message data.
clientSocket.send("From: {}\nTo: {}\nSubject: {}\n".format(SenderEmail, ReceiverEmail, Subject).encode())
clientSocket.send(b'Content-Type: multipart/mixed; boundary = "<END>"\r\n\r\n')
clientSocket.send(b'--<END>\r\n')
clientSocket.send(b'Content-Type: text/plain; charset =UTF-8; format=flowed\r\n\r\n')
clientSocket.send(msg.encode(FORMAT) + b'\r\n')

# Send file
sendFile(clientSocket)

# End email
clientSocket.send(b'--<END>--\r\n.\r\n')
confMsg8 = clientSocket.recv(1024).decode()
print(confMsg8)

# Send QUIT command and get server response.
quitcommand = 'QUIT\r\n'
clientSocket.send(quitcommand.encode())
confMsg9 = clientSocket.recv(1024).decode()
print(confMsg9)



clientSocket.close()
print('Was successful!')