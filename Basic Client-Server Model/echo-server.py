import socket
HOST = '127.0.0.1'
PORT = 65430

QuesNResp = {
    'Hello': 'Hey! How can i help you?', 
    'Hi': 'Hey! How can i help you?',
    'Please Help Me': 'Tell me, what is the issue?'
}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    while True:
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f'Connected with {addr}')
            data = conn.recv(1024)
            if not data:
                break
            data = data.decode('utf-8')
            msg = QuesNResp[data]
            conn.sendall(msg.encode('utf-8'))