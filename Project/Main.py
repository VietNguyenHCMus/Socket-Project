import json
import SendMail
import ReceiveMail


def main():
    with open('General.json', 'r') as file:
        data = json.load(file)
    user = data['user']
    server = data['server']
    user_ip = input('Enter username: ')
    user_pass = input('Enter password: ')
    if user_ip in user:
        if user[user_ip] == user_pass:
            print('Login successfully')
        else: 
            return
    else:
        return

    while True:
        choose = input('Menu\n1. Send Mail\n2. Receive Mail\n3. Exit\nYour choice: ')
        if choose == "1":
            SendMail.sendMail(server["HOST"],int(server["SMTP"]),user_ip)
        elif choose == '2':
            ReceiveMail.receiveMail(server["HOST"], int(server["POP3"]), user_ip, user_pass)
        elif choose == '3':
            break
        else:
            print('Nhap lai di!')
    
    print('Exit Successfully!')
    
if __name__ == "__main__":
    main()