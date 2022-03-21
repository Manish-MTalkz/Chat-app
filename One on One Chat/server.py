# Code for the server side of the One on One Chat

# Importing the Libraries
import socket
import threading


# Creating a class Server which handle all its related functions
class Server:
    def __init__(self):
        self.__start_server()

    """
        start_server() is used to create an instance socket class to start the server 
        on the local machine.
    """

    def __start_server(self):
        """
            AF_NET is used for the host on which on server will run, mostly on IPV4.
            SOCK_STREAM is used for the continuous flow of the data from the client to server.
        """
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        """
            getHostByName() returns the IP Address of the server. getHostName() returns the host name of
            the current system under which the python interpreter is executed.
        """
        host = socket.gethostbyname(socket.gethostname())
        port = int(input('Enter port to run the server on ---> '))

        # To check availability of the clients connected to the server
        self.clients = []

        """
            bind() function is used to associate the socket with local address, i.e. IP Address, port and
            address family.
        """
        self.s.bind((host, port))
        # listen() function indicates the readiness of the server to connect with the client
        self.s.listen(100)

        print('Running on host:', host)
        print('Running on port:', port)

        self.username_lookup = {}
        self.connection_lookup = {}

        while True:
            conn, addr = self.s.accept()

            # Getting username of the client
            username = conn.recv(1024).decode()

            print('New Connection. Username: ' + str(username))
            self.__broadcast('New Person joined the room. Username: ' + username)
            # Saving the username of the client as per the connection
            self.username_lookup[conn] = username
            # Saving the client object for the username as per the connection
            self.connection_lookup[username] = conn
            # Appending the available client in the clients
            self.clients.append(conn)
            # Creating thread
            threading.Thread(target=self.__handle_clients, args=(conn, addr)).start()

    # broadcast() is used to send the msg to all the clients connected in the chatroom.
    def __broadcast(self, msg):
        for client in self.clients:
            client.send(msg.encode())

    """
        handle_client() is used to retrieve the message sent by the client and broadcast 
        the message to all other clients.
    """

    def __handle_clients(self, conn, addr):
        while True:
            try:
                msg = conn.recv(1024)
            except:
                # socket.SHUT_RDWR shuts down one or both halves of the connection
                conn.shutdown(socket.SHUT_RDWR)
                # Removing the client from client available list
                self.clients.remove(conn)
                print(str(self.username_lookup[conn]) + ' left the room.')
                self.__broadcast(str(self.username_lookup[conn]) + ' has left the room.')

                break

            # conn has some message, it should be sent to all other clients than itself.
            if msg.decode() != '':
                info = msg.decode().split()
                # joint() takes all the item in iterable and joins them in a string.
                client2, msg = str(info[2]), ' '.join(info[3:])
                overallMsg = str(self.username_lookup[conn]) + ' -> ' + str(msg)
                print(overallMsg)
                connection2 = self.connection_lookup.get(client2, None)
                if connection2 is None:
                    msg = client2 + ' is not present. Please try again later.'
                    conn.send(msg.encode())
                else:
                    connection2.send(overallMsg.encode())

server = Server()