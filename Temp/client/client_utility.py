from client_libraries import *

# Creating an instance of the customer class
def create_customer_object():
    username = input('Please enter your name: ')
    new_customer = customer(username)
    print(username + ' has been connected as ' + new_customer.type)
    return new_customer

# Creating an instance of the field_agent class and saving username and password in the database
def create_field_agent_object(username, password):
    new_field_agent = field_agent(username)     # Creating an instance of field_agent 
    print(username + ' has been connected as ' + new_field_agent.type)
    return new_field_agent                      # Returning the instance of field_agent

# Creating the database connection for the client for the authentication
def create_database_connection():
    # Creating a connection object to connect with database
    database_connector = psycopg2.connect(database = 'mtalkz', user = 'postgres', password = '123456', 
                                            host = '127.0.0.1', port = 5432)
    return database_connector   # Returning the connector

# Authentication of the field agent in the database
def authenticate(username, password):
    database_connector = create_database_connection() # Getting the connector for the database connection
    cursor = database_connector.cursor()
    # Executing SQL statement
    cursor.execute('SELECT * FROM auth_table where username = %s',(username,))
    data = cursor.fetchone()
    if data[0] == username and data[1] == password:
        return True
    else:
        return False

# Saving the username and password in the database
def save_to_the_database(username, password):
    database_connector = create_database_connection() # Getting the connector for the database connection
    cursor = database_connector.cursor()
    # Executing SQL Command
    cursor.execute('INSERT INTO auth_table VALUES(%s, %s)', (username,password))
    database_connector.commit()
    print('Username and password has been saved to the database')

# Login function for the field agent
def login(username, password):
    success = authenticate(username,password)
    if success is True:
        print('Login Successful')
        agent = create_field_agent_object(username,password)
        create_connection_to_the_server(agent)
    else:
        print('Wrong username and password. Please try it again.')

"""
    Requesting the server to accept the request from the client side in order to connect the customer
    with field agent.
"""
def create_connection_to_the_server(class_object):
    # Creating an instance of the socket for the connecting the client with server
    server_connector = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.1.1'                                          # Host of the Server on which it is running
    while True:
        try:
            port = int(input('Please enter the socket no: '))   # Taking port no as input
            server_connector.connect((host,port))               # Sending connecting request to the server
            break        
        except:     # In case, the connector is not able to bind host with port
            print('There is some problem in connecting the server, please try again.')
    
    # Sending a message
    message_from_client = 'Please accept ' + class_object.username + ' as ' + class_object.type
    server_connector.send(message_from_client.encode())

    create_threads(server_connector)    # Creating Threads for functions

# Creating threads for various functions that client have to handle
def create_threads(connector):
    # Creating thread for recieving and sending the messages from client to server or vice a versa
    message_handler = threading.Thread(target = handle_messages, args = (connector,))
    input_handler = threading.Thread(target = handle_input, args = (connector,))
    message_handler.start()
    input_handler.start()

# Creating a function for sending the messages to the server
def handle_messages(connector):
    while True:
        msg_to_server = input()                 # Recieving the message from the client
        encoded_msg = msg_to_server.encode()    # Encoding is used to send the message in bits
        connector.send(encoded_msg)             # Sending messsage to the server

# Create a function for accepting the messages from the server
def handle_input(connector):
    while True:
        msg_from_server = connector.recv(1024)  # Recieving the message from the server   
        decoded_msg = msg_from_server.decode()  # Decoding the message
        print(decoded_msg)                      # Printing the decoded the message