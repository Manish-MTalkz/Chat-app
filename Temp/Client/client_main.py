from client_utility import *

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

# Menu for the Field Agent
def menu_for_field_agent():
    print('1. Do you want to login ?')
    print('2. Do you want to sign up as a new agent?')
    choice = int(input('Please enter the choice: '))
    username = input('Please enter the username: ')
    password = input('Please enter the password: ')
    if choice == 1:
        login(username,password)
    elif choice == 2:
        new_field_agent = create_field_agent_object(username,password)  # Creating the instance of field_agent
        save_to_the_database(username,password) # Saving username and password to the database for future authentication
        """
            After creating the instance of the customer, we are sending the request to the server to 
            accept the client as a field agent.
        """
        create_connection_to_the_server(new_field_agent)
    else:
        print('Wrong choice entered. Please try it again.')

""" 
    main_menu() function is for creating the menu for the client whether 
    the client is customer or the field agent.
"""
def main_menu():
    print('<----- Main Menu ----->')
    print('1. Customer')
    print('2. Field Agent')
    designation = int(input('Please enter the choice: '))

    if designation == 1:                            # All the functions related to the customer
        new_customer = create_customer_object()     # Instance of the customer class
        """
            After creating the instance of the customer, we are sending the request to the server to 
            accept the client as a customer.
        """
        create_connection_to_the_server(new_customer)
    elif designation == 2:
        menu_for_field_agent()
    else:
        print('Wrong Designation Entered. Please try it again.')

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
    msg_to_server = input()                 # Recieving the message from the client
    encoded_msg = msg_to_server.encode()    # Encoding is used to send the message in bits
    connector.send(encoded_msg)             # Sending messsage to the server

# Create a function for accepting the messages from the server
def handle_input(connector):
    msg_from_server = connector.recv(1024)  # Recieving the message from the server   
    decoded_msg = msg_from_server.decode()  # Decoding the message
    print(decoded_msg)                      # Printing the decoded the message