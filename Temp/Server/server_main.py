from server_utility import *

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
        username,type = useful_data[2],useful_data[-1]      # Getting username and its type from useful_data
        # add_client_to_the_database(username,type)           # Adding client to the database

        if type == 'field_agent':
            new_agent = field_agent(username,connection)        # Creating a new instance for the field_agent class
            field_agent_available.append(new_agent)             # Adding the new_agent to the field_agent_available
            """
                Adding connection object for the field agent in the dictionary so that 
                username of the agent can be searched as per the connection object.
            """
            connection_with_field_agent[connection] = username  
            print(username + ' has joined the server as ' + type)
            print('All the field agents available on the Server')
            print_all_names(field_agent_available)              # Printing username of all the field agents available
        else:
            new_customer = customer(username,connection)        # Creating a new instance for the customer class
            customer_available.append(new_customer)             # Adding the customer to the customer_available
            """
                Adding connection object for the customer in the dictionary so that
                username of the customer can be searched as per the connection object.
            """
            connection_with_customer[connection] = username
            print(username+ ' has joined the server as ' + type)
            print('All the customers available on the Server')
            print_all_names(customer_available)                 # Printing username of all the customers available
            create_connection_btw_customer_n_field_agent()        # Creating connection between the customers and field agents
        
        # Creating a thread for handling the client
        client_handler = threading.Thread(target = handle_client, args = (connection,address,username,type))
        client_handler.start()