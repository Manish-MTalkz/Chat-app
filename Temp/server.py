import socket
import threading


class Server:
    def __init__(self):
        self.__customers = []
        self.__fieldAgents = []
        self.__start_server()

    def __start_server(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostbyname(socket.gethostname())
        port = int(input('Enter port to run the server on --> '))

        self.s.bind((host, port))
        self.s.listen(100)

        print('Running on host:', host)
        print('Running on port:', port)

        while True:
            conn, addr = self.s.accept()
            type = conn.recv(1024).decode().split()[-1]
            if type == 'CUSTOMER':
                self.__customers.append(conn)
            else:
                self.__fieldAgents.append(conn)

        handle_clients = threading.Thread(target=self.__handle_clients, arg=())
        handle_clients.start()

    def __handle_clients(self, conn, addr, type):
        while True:
            try:
                msg = conn.recv(1024)
            except:
                conn.shutdown(socket.SHUT_RDWR)
                if type == 'CUSTOMER':
                    self.__customers.remove(conn)
                else:
                    self.__fieldAgents.remove(conn)
                break
            if msg.decode() != '':
                msg = msg.decode()
                print(msg)


server = Server()