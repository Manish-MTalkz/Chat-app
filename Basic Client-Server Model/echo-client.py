import socket
HOST = '127.0.0.1'
PORT = 65430

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    str = input()
    s.sendall(str.encode('utf-8'))
    data = s.recv(1024)
print(f'Recieved {data!r}')