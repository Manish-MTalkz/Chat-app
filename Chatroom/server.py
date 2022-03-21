# Code for the server side of the chat room

# Importing the Libraries
import socket
import threading

"""
    Creating a Server Class which handles its different function from handling the client 
    to broadcasting the msg.
"""
class Server:
    # Constructor
    def __init__(self):
        self.start_server()

    # Start_Server function initialises the object for the server
    def start_server(self):
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
        port = int(input('Enter port to run the server on --> '))

        # List of the clients connected to the server.
        self.clients = []

        """
            bind() function is used to associate the socket with local address, i.e. IP Address, port and
            address family.
        """
        self.s.bind((host, port))
        # listen() function indicates the readiness of the server to connect with the client
        self.s.listen(100)

        print('Running on host: ' + str(host))
        print('Running on port: ' + str(port))

        self.username_lookup = {}

        # In order to run the server for the infinite times
        while True:
            c, addr = self.s.accept()

            # Getting username of the client
            username = c.recv(1024).decode()

            print('New connection. Username: ' + str(username))
            self.broadcast('New person joined the room. Username: ' + username)

            # Saving the username of the client as per the connection
            self.username_lookup[c] = username
            # Appending the available client in the clients
            self.clients.append(c)
            # Creating thread
            threading.Thread(target=self.handle_client, args=(c, addr,)).start()

    # broadcast() is used to sent the msg all over the clients connected in the chatroom.
    def broadcast(self, msg):
        for connection in self.clients:
            connection.send(msg.encode())

    """
        handle_client() is used to retrieve the message sent by the client and broadcast 
        the message to all other clients.
    """

    def handle_client(self, c, addr):
        while True:
            try:
                msg = c.recv(1024)
            except:
                # socket.SHUT_RDWR shuts down one or both halves of the connection
                c.shutdown(socket.SHUT_RDWR)
                # Removing the client from client available list
                self.clients.remove(c)

                print(str(self.username_lookup[c]) + ' left the room.')
                self.broadcast(str(self.username_lookup[c]) + ' has left the room.')

                break

            # c has some message, it should be sent to all other clients than itself.
            if msg.decode() != '':
                print('New message: ' + str(msg.decode()))
                for connection in self.clients:
                    if connection != c:
                        connection.send(msg)


# Creating an instance of the server
server = Server()