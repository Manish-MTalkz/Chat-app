# Code for the client side for the chat room

# Importing the Libraries
import socket
import threading

"""
    Creating a Client Class which handles all the functions related to the 
    client in the chat room. 
"""

class Client:
    # Constructor
    def __init__(self):
        self.__create_connection()

    # create_connection is used to the client to the server
    def __create_connection(self):
        # Creating an instance of socket as client
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while 1:
            try:
                host = input('Enter host name --> ')
                port = int(input('Enter port --> '))
                self.s.connect((host, port))

                break
            except:
                print("Couldn't connect to server")

        self.username = input('Enter username --> ')
        self.s.send(self.username.encode())

        # Creating thread for retrieving the messages
        message_handler = threading.Thread(target=self.__handle_messages, args=())
        message_handler.start()

        # Creating thread for sending the messages
        input_handler = threading.Thread(target=self.__input_handler, args=())
        input_handler.start()

    def __handle_messages(self):
        while 1:
            print(self.s.recv(1204).decode())

    def __input_handler(self):
        while 1:
            self.s.send((self.username + ' - ' + input()).encode())

# Creating the instance of the client
client = Client()