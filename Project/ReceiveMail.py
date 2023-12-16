import socket
import os
import base64
format = "utf-8"

#chuadoc
def check_doc(data):
    if data[-7:] == 'chuadoc': return 1
    return 0


def Doc_Thu(folder, list_from, list_sub):
    list_data = []

    for i in range(len(os.listdir(folder))):
        with open(folder + '\Mail' + str(i + 1) + '.txt', 'r') as attachment_file:
            attachment_data = attachment_file.read()
        data = attachment_data  # Mã hóa base64
        list_data.append(data)

    for i in range (len(list_data)):
        if (check_doc(list_data[i]) == 1):
            print('(chưa đọc)' + str(i+1) + '. <' + list_from[i] + '>, <' + list_sub[i] + '>')
        else:
            print(str(i+1) + '. <' + list_from[i] + '>, <' + list_sub[i] + '>')
    
    check = int(input('\nBạn muốn đọc Email thứ mấy (hoặc nhấn enter để thoát ra ngoài, hoặc nhấn 0 để xem lại danh sách email): '))
    if (check != 0):
        print('Nội dung email của email thứ ' + str(check) + ': ')
        # lấy nội dung email:
        print(list_data[0])
        data_idx = list_data[check-1].find('Content-Type:text/plain;charset=UTF-8;format=flowed') + len('Content-Type:text/plain;charset=UTF-8;format=flowed\r\n\r\n')
        if (list_data[check-1].find('Content-Transfer-Encoding: base64') != -1): # có file đính kèm
            data_idx_end = list_data[check -1].find('--boundary', data_idx);
            data_res = list_data[check -1][data_idx : data_idx_end]
            print(data_res)
        else: # không có file đính kèm
            data_idx_end = list_data[check -1].find('--boundary--', data_idx)
            data_res = list_data[check -1][data_idx : data_idx_end]
            print(data_res)
        
        if (list_data[check-1].find('Content-Transfer-Encoding: base64') == -1): return; # kh có attachment file
    

        char = input('Trong email này có attached file, bạn có muốn save không : ')
        if (char == 'có' or char == 'co'):
            path = input('Cho biết đường dẫn bạn muốn lưu (nhập thêm kí tự \ vào cuối): ')

            # xác định nếu có file đính kèm và lấy thong tin file:
            pos = 0
            i = 0
            num_file = list_data[check -1].count('Content-Transfer-Encoding: base64')
            attachment_start = -1
            while (list_data[check -1].find('Content-Transfer-Encoding: base64', pos) != -1):
                attachment_start = list_data[check -1].find('Content-Transfer-Encoding: base64', pos)
                if attachment_start != -1: # có file
                    i += 1
                    idx_start = attachment_start + len('Content-Transfer-Encoding: base64\r\n\r\n'); # cho \r\n\r\n
                    idx_end = 0
                    if (i != num_file):
                        idx_end = list_data[check -1].find('--boundary', idx_start)
                    else:
                        idx_end = list_data[check -1].find('--boundary--')
                    res = list_data[check -1][idx_start : idx_end]

                    # print(res)
                    #tên file đính kèm:
                    attachment_file = ''
                    if (list_data[check -1].find('Content-Type:application/octet-stream', pos, idx_end) != -1):
                        attachment_file = 'download.txt'
                    elif (list_data[check -1].find('Content-Type:application/pdf', pos, idx_end) != -1):
                        attachment_file = 'download.pdf'
                    elif(list_data[check -1].find('Content-Type:application/msword', pos, idx_end) != -1):
                        attachment_file = 'download.docx'
                    elif (list_data[check -1].find('Content-Type:image/jpeg', pos, idx_end) != -1):
                        attachment_file = 'download.jpg'
                    elif (list_data[check -1].find('Content-Type:application/zip', pos, idx_end) != -1):
                        attachment_file = 'download.zip'

                    # print(attachment_file)
                    # kiểm tra -> tạo file -> ghi dữ liệu vào:
                    if not os.path.exists(path + attachment_file):
                        with open(attachment_file, "xb") as attachment_file: # xb : kiểm tra nếu chưa có file đó thì tạo ra file mới tự động, còn có rồi thì kh thực hiện
                            attachment_file.write(base64.b64decode(res))
                    else:
                        print('file alredy exist');

                    pos = idx_end
    
    # đổi lại mail này thành mail đã đọc:
    if (check_doc(list_data[check -1]) == 1):
        with open(folder + '\\Mail' + str(check) + '.txt', "w") as attachment_file: # wb : mở file, xóa nd cũ, ghi nd mới
            attachment_file.write(list_data[check-1].replace('chuadoc', 'dadoc'))

# HET HAM DOC THU ----------------------------------------------------------------------------------------------------




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

    while (1):
        choose = input('Bạn muốn xem email trong folder nào (Nhấn enter để thoát ra ngoài): ')

        if (not choose):
            break
        elif choose == '1':
            Doc_Thu('Inbox', list_sender, list_subject)
        elif choose == '2':
            Doc_Thu('Project', list_sender, list_subject)
        elif choose == '3':
            Doc_Thu('Important', list_sender, list_subject)
        elif choose == '4':
            Doc_Thu('Work', list_sender, list_subject)
        elif choose == '5':
            Doc_Thu('Spam', list_sender, list_subject)

