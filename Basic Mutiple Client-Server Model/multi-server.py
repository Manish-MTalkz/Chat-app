"""
A Multi Client Server which connects client with the help of the threading
"""

# Importing the Libraries
import socket
import os
from _thread import *


# Connecting multiple clients with the server
def multi_threaded_client(connection):
    connection.send(str.encode('Server is working:'))  # Sending a message to the client that it is connected to server
    # Receiving the data from the client
    while True:
        data = connection.recv(1024)
        response = 'Server message: ' + data.decode('utf-8')
        if not data:
            break
        else:
            # Sending the response
            connection.sendall(str.encode(response))
    connection.close()


ServerSideSocket = socket.socket()  # Creating an instance of class socket
host = '127.0.0.1'  # Address of server
port = 2004  # Port of the server on the device
ThreadCount = 0  # No of Clients running parallely

# Connecting HOST with PORT
try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))
print('Socket is listening.....')
ServerSideSocket.listen(5)

# To make the server run constantly, we are running the server in an infinite loop
while True:
    Client, Address = ServerSideSocket.accept()
    print('Connected to: ' + Address[0] + ':' + str(Address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

ServerSideSocket.close()