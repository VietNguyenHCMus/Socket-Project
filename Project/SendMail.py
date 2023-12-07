# Portable password input
from getpass import getpass
from socket import *
import ssl

SenderEmail = input("Enter Your Email Address: ")
# SenderPassword = getpass("Enter Your Password: ")  # Commented out to remove password input
ReceiverEmail = input("Enter Email Destination: ")
Subject = input("Enter Email Subject: ")
EmailBody = input("Enter Email Body Message: ")

# Message included in body
msg = '{}. \r\nI love computer networks!'.format(EmailBody)
endmsg = '\r\n.\r\n'

# Choose a mail server (e.g., Google mail server) and call it mailserver
server_address = ('localhost', 2225)

# Fill in start
# Creating socket called clientSocket
clientSocket = socket(AF_INET, SOCK_STREAM)

# Establishing a TCP connection with mailserver
clientSocket.connect(server_address)
# Fill in end

confMsg = clientSocket.recv(1024)
print(confMsg)
if confMsg[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'.encode()
clientSocket.send(heloCommand)
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
clientSocket.send("Subject: {}\n\n{}".format(Subject, msg).encode())

# Message ends with a single period.
clientSocket.send(endmsg.encode())
confMsg8 = clientSocket.recv(1024).decode()
print(confMsg8)

# Send QUIT command and get server response.
quitcommand = 'QUIT\r\n'
clientSocket.send(quitcommand.encode())
confMsg9 = clientSocket.recv(1024).decode()
print(confMsg9)

clientSocket.close()
print('Was successful!')