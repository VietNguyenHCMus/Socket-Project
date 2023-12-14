import socket
import base64

FORMAT ='utf-8'

def send_file(file_path, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        # Send file name
        file_name = file_path.split("/")[-1]  # Extracting just the file name
        s.sendall(file_name.encode())
        
        # Wait for acknowledgment from receiver
        s.recv(1024)
        
        # Send file data
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                
        encoded_attachment = base64.b64encode(data).decode(FORMAT)
        s.sendall(encoded_attachment.encode(FORMAT))
        print(f"File '{file_name}' has been sent.")

if __name__ == "__main__":
    file_to_send = 'vay.png'  # Replace this with your file path
    destination_host = '127.0.0.1'  # Replace with the receiver's IP address
    destination_port = 3335  # Replace with the port the receiver is listening on
    
    send_file(file_to_send, destination_host, destination_port)
