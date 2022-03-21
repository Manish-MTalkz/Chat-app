# IMPORTING THE LIBRARIES
import socket
import threading

FIELD_AGENTS = [] # All the field agents available on the server
CUSTOMERS = [] # All the customers available on the server

class FIELD_AGENT:
    pass

class CUSTOMER:
    pass

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname(socket.gethostbyname())
    port = int(input('Enter port to run the server on --> '))
    s.bind((host,port))
    s.listen(100)
    print('Running on host: ', host)
    print('Running on port: ', port)

    while True:
        conn, addr = s.accept()
        msg = conn.recv(1024).decode()
        client_handler = threading.Thread(target = handle_clients, args = (conn, addr, msg))
        client_handler.start()

def handle_clients(conn, addr, msg):
    pass