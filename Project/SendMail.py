from socket import *
from Sendfile import sendFile

FORMAT = 'utf-8'

def sendMail(localhost, PORT, SenderEmail):
    server_address = (localhost, PORT)
    print("Đây là thông tin soạn email: (nếu không điền vui lòng nhấn enter để bỏ qua)")
    ReceiverEmail = input("TO: ")
    Subject = input("SUBJECT: ")
    EmailBody = input("CONTENT: ")

    # Message included in body
    msg = '{}. \r\n'.format(EmailBody)

    # Fill in start
    # Creating socket called clientSocket
    clientSocket = socket(AF_INET, SOCK_STREAM)

    # Establishing a TCP connection with mailserver
    clientSocket.connect(server_address)

    confMsg = clientSocket.recv(1024)

    # Send HELO command and print serverresponse.
    heloCommand = 'EHLO ' + localhost + '\r\n'
    clientSocket.send(heloCommand.encode())
    recv1 = clientSocket.recv(1024).decode()

    # Send MAIL FROM command and print server response.
    mailfrom = "MAIL FROM: <{}>\r\n".format(SenderEmail)
    clientSocket.send(mailfrom.encode())
    confMsg5 = clientSocket.recv(1024).decode()

    # Send RCPT TO command and print server response.
    rcptto = "RCPT TO: <{}>\r\n".format(ReceiverEmail)
    clientSocket.send(rcptto.encode())
    confMsg6 = clientSocket.recv(1024).decode()


    # Send DATA command and print server response.
    data = 'DATA\r\n'
    clientSocket.send(data.encode())
    confMsg7 = clientSocket.recv(1024).decode()

    # Send message data.
    clientSocket.send("From: {}\nTo: {}\nSubject: {}\n".format(SenderEmail, ReceiverEmail, Subject).encode())
    clientSocket.send(b'Content-Type: multipart/mixed; boundary = "boundary"\r\n\r\n')
    clientSocket.send(b'--boundary\r\n')
    clientSocket.send(b'Content-Type: text/plain; charset =UTF-8; format=flowed\r\n\r\n')
    clientSocket.send(msg.encode(FORMAT) + b'\r\n')

    # Send file
    sendFile(clientSocket)

    # End email
    clientSocket.send(b'--boundary--\r\n.\r\n')
    confMsg8 = clientSocket.recv(1024).decode()


    # Send QUIT command and get server response.
    quitcommand = 'QUIT\r\n'
    clientSocket.send(quitcommand.encode())
    confMsg9 = clientSocket.recv(1024).decode()

    clientSocket.close()
    print('Đã gửi email thành công\n')
    
if __name__ == "__main__":
    sendMail()
