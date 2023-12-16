import PO3Mail
from SendMail import sendMail
import socket

localhost = '127.0.0.1'
IP = 2225

# Tạo một socket của client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Kết nối đến server qua địa chỉ và cổng
server_address = (localhost, IP)

def main():
    temp = int()
    while(temp != 3):
        print("Vui long chon Menu: ")
        print("1. Để gửi email")
        print("2. Để xem danh sách các email đã nhận")
        print("3. Thoát")
        choice = int(input("Bạn chọn: "))
        while(choice):
            if(choice == 1): 
                sendMail(server_address)
                break
            if(choice == 2):
                break
            if(choice == 3):
                temp = choice
                break
            break
        
if __name__ == '__main__':
    main()
        