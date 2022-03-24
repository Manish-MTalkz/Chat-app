# Server Side Code for the Chat app
# Importing the Libraries
import socket       # socket library is used for creating the connection between client and server
import threading    # threading library is used for creating threads of the various functions in the server and entcli
import psycopg2     # psycopg2 library is used for connecting server to the database

#<------------------------------------- Class for Customer and Field Agent ----------------------------------------->#

# Creating the class for the customer for all its features and handle its functionality
class customer:
    def __init__(self, username):
        self.username = username
        self.type = 'customer'

# Creating the class for the field_agent for all its features and handle its functionality
class field_agent:
    def __init__(self, username, connection):
        self.username = username
        self.connection = connection
        self.type = 'field_agent'

#<------------------------------------------------ Main Function --------------------------------------------------->#

"""
    start_server() function is for enabling server to accept the connections from the client and handle as per
    requirement
"""
def start_server():
    # Creating an instance of the socket for connecting the server to client
    client_connector = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """
        getHostByName() returns the IP Address of the server. getHostName() returns the host name of
        the current system under which the python interpreter is executed.
    """
    host = socket.gethostbyname(socket.gethostname())
    port = int(input('Please enter the port number: '))     # Getting port no from the user on which server will run
    client_connector.bind((host,port))                      # Binding the host and port
    client_connector.listen(100)                            # listen() function indicates the readiness of the server 
                                                            # to connect with the client

    # Accepting the connection requests from clients
    while True:
        connection, address = client_connector.accept()     # Getting connection object and address from the client 
        msg_from_client_encoded = connection.recv(1024)     # Getting the encoded message from the client
        msg_from_client_decoded = msg_from_client_encoded.decode()
        print(msg_from_client_decoded)
        useful_data = msg_from_client_decoded.split()       # Fetching useful data from the msg_from_client
        username,type = useful_data[3],useful_data[-1]      # Getting username and its type from useful_data
        add_client_to_the_database(username,type)           # Adding client to the database

        if type == 'field_agent':
            new_agent = field_agent(username,connection)    # Creating a new instance for the field_agent class
        else:
            new_customer = customer(username,connection)    # Creating a new instance for the customer class

# Creating the database connection for the server
def create_database_connection():
    # Creating a connection object to connect with the database
    database_connector = psycopg2.connect(database = 'mtalkz', user = 'postgres', password = '123456',
                                            host = '127.0.0.1', port = 5432)
    return database_connector       # Returning the connector

# function for adding the client to the database of the server
def add_client_to_the_database(username, type):
    database_connector = create_database_connection()       # Getting connector object to connect with database
    cursor = database_connector.cursor()
    # Executing the SQL command and inserting username and its type into the database
    cursor.execute('INSERT INTO clients VALUES(%s, %s)', (username,type))   
    database_connector.commit()

start_server()