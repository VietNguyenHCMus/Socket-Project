import os
import base64

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


