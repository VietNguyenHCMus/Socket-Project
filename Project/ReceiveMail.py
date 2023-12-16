import socket
import os
import base64
format = "utf-8"

def read_emails(folder, sender_list, subject_list):
    emails_data = []

    # Read email data from files in the specified folder
    for i in range(len(os.listdir(folder))):
        with open(f"{folder}\\Mail{i + 1}.txt", 'r') as file:
            email_data = file.read()
        emails_data.append(email_data)

    # Display email list with read/unread status
    for i, email in enumerate(emails_data, start=1):
        status = "(unread)" if check_if_unread(email) else ""
        print(f"{status}{i}. <{sender_list[i - 1]}>, <{subject_list[i - 1]}>")

    # Choose an email to read
    email_choice = int(input("\nEnter the number of the email to read "
                             "(or press Enter to exit, or 0 to see the list again): "))

    if email_choice == 0:
        return
    elif 1 <= email_choice <= len(emails_data):
        print(f"\nEmail content of email {email_choice}: ")
        print(emails_data[email_choice - 1])

        # Extract email content
        email_content = emails_data[email_choice - 1]
        content_start = email_content.find('Content-Type:text/plain;charset=UTF-8;format=flowed') + len('Content-Type:text/plain;charset=UTF-8;format=flowed\r\n\r\n')

        # Check for attached files
        if 'Content-Transfer-Encoding: base64' in email_content:
            content_end = email_content.find('--boundary', content_start)
            content = email_content[content_start: content_end]
            print(content)

            # Prompt to save attached file
            user_input = input('This email contains an attached file. Do you want to save it: ')
            if user_input.lower() in ['yes', 'y']:
                save_attachment(email_content, email_choice)

        # Mark the email as read
        mark_as_read(folder, email_choice, emails_data[email_choice - 1])

def check_if_unread(email_data):
    return 'unread' in email_data

def save_attachment(email_content, email_choice):
    path = input('Specify the path to save the attachment (add \ at the end): ')
    position = 0
    file_counter = email_content.count('Content-Transfer-Encoding: base64')

    while 'Content-Transfer-Encoding: base64' in email_content[position:]:
        attachment_start = email_content.find('Content-Transfer-Encoding: base64', position)
        if attachment_start != -1:
            file_counter -= 1
            start_index = attachment_start + len('Content-Transfer-Encoding: base64\r\n\r\n')
            end_index = 0
            if file_counter != 0:
                end_index = email_content.find('--boundary', start_index)
            else:
                end_index = email_content.find('--boundary--')
            attachment_data = email_content[start_index: end_index]

            attachment_name = determine_attachment_type(email_content, position, end_index)

            if not os.path.exists(path + attachment_name):
                with open(attachment_name, "xb") as attachment_file:
                    attachment_file.write(base64.b64decode(attachment_data))
            else:
                print('File already exists')

            position = end_index

def determine_attachment_type(email_content, start, end):
    attachment_types = {
        'application/octet-stream': 'download.txt',
        'application/pdf': 'download.pdf',
        'application/msword': 'download.docx',
        'image/jpeg': 'download.jpg',
        'application/zip': 'download.zip'
    }

    for content_type, file_name in attachment_types.items():
        if content_type in email_content[start:end]:
            return file_name

def mark_as_read(folder, email_number, email_data):
    if check_if_unread(email_data):
        with open(f"{folder}\\Mail{email_number}.txt", "w") as file:
            file.write(email_data.replace('unread', 'read'))





def receiveMail(Host, port, username, password):
    
    current = os.getcwd()
    user_path = os.path.join(current, username)
    if os.path.exists(user_path) == False:
        os.makedirs(username)
        os.mkdir(os.path.join(user_path, 'Inbox'))
        os.mkdir(os.path.join(user_path, 'Work'))
        os.mkdir(os.path.join(user_path, 'Important'))
        os.mkdir(os.path.join(user_path, 'Spam'))
        os.mkdir(os.path.join(user_path, 'Project'))
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((Host, int(port)))
    response = client.recv(1024).decode()
    client.send('USER {}\r\n'.format(username).encode(format))
    response = client.recv(1024).decode()
    client.send('PASS {}\r\n'.format(password).encode(format))
    response = client.recv(1024).decode()
    client.send('STAT\r\n'.encode(format))
    response = client.recv(1024).decode()
    client.send('LIST\r\n'.encode(format))
    response = client.recv(1024).decode()
    client.send('UIDL\r\n'.encode(format))
    response = client.recv(1024).decode()
    
    list_name_mail = [item.split(' ')[1] for item in response.splitlines()[1:-1]]
    
    list_sender, list_subject = [], []
    for i in range(len(list_name_mail)):
        client.send('RETR {}\r\n'.format(i+1).encode(format))
        data = ""
        while True:
            response = client.recv(1024)
            data += response.decode()
            if b'\r\n.\r\n' in response: break
        
        from_start_idx = data.find('From:') + len('From:') + 1
        from_end_idx = data.find('To:')
        list_sender.append(data[from_start_idx : (from_end_idx - len('\r\n'))])

        subject_start_idx = data.find('Subject:') + len('Subject:') + 1
        subject_end_idx = data.find('Content')
        list_subject.append(data[subject_start_idx : (subject_end_idx - len('\r\n'))])
        ################################################################################################

        # Xu ly loc mail:
        if (list_sender[i] == 'ahihi@testing.com' or list_sender[i] == 'ahuu@testing.com'):
            folder_path = os.path.join(os.path.join(user_path, 'Project'))
            cnt = len(os.listdir(folder_path))
            file_path = os.path.join(folder_path,str(cnt+1))
            with open(file_path, "w") as attachment_file: 
                attachment_file.write(data + 'chuadoc')
        elif (list_subject[i] == 'urgent' or list_subject[i] == 'ASAP'):
            folder_path = os.path.join(os.path.join(user_path, 'Important'))
            cnt = len(os.listdir(folder_path))
            file_path = os.path.join(folder_path,str(cnt+1))
            with open(file_path, "w") as attachment_file: 
                attachment_file.write(data + 'chuadoc')
        elif (data.find('report') != -1 or data.find('meeting') != -1):
            folder_path = os.path.join(os.path.join(user_path, 'Work'))
            cnt = len(os.listdir(folder_path))
            file_path = os.path.join(folder_path,str(cnt+1))
            with open(file_path, "w") as attachment_file: 
                attachment_file.write(data + 'chuadoc')
        elif (list_subject[i] == 'virus' or list_subject[i] == 'hack' or list_subject[i] == 'crack'):
            folder_path = os.path.join(os.path.join(user_path, 'Spam'))
            cnt = len(os.listdir(folder_path))
            file_path = os.path.join(folder_path,str(cnt+1))
            with open(file_path, "w") as attachment_file: 
                attachment_file.write(data + 'chuadoc')
        else:
            folder_path = os.path.join(os.path.join(user_path, 'Inbox'))
            cnt = len(os.listdir(folder_path))
            file_path = os.path.join(folder_path,str(cnt+1))
            with open(file_path, "w") as attachment_file: 
                attachment_file.write(data + 'chuadoc')
        
        client.send('DELE {}\r\n'.format(i+1).encode(format))
        response = client.recv(1024).decode()
    
    client.send('QUIT\r\n'.encode(format))
    client.recv(1024).decode()




    print('Nhan thu thanh cong!')
    print('Đây là danh sách các folder trong mailbox của bạn: ')
    print('1. Inbox')
    print('2. Project')
    print('3. Important')
    print('4. Work')
    print('5. Spam')
    

    current = os.getcwd()
    user_path = os.path.join(current, username)
    if os.path.exists(user_path) == True:
        while (1):
            choose = input('Bạn muốn xem email trong folder nào (Nhấn enter để thoát ra ngoài): ')
            if (not choose):
                break
            elif choose == '1':
                read_emails('Inbox', list_sender, list_subject)
            elif choose == '2':
                read_emails('Project', list_sender, list_subject)
            elif choose == '3':
                read_emails('Important', list_sender, list_subject)
            elif choose == '4':
                read_emails('Work', list_sender, list_subject)
            elif choose == '5':
                read_emails('Spam', list_sender, list_subject)

