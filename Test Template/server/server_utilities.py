from server_libraries import *

field_agent_available = []          # All the field agents available on the server
customer_available = []             # Al the customers available on the server
connection_with_field_agent = {}    # Creating a mapper with locating connection object with field agent username
connection_with_customer = {}       # Creating a mapper with locating connection object with customer username

# Function to print the username of the field agent and customer available
def print_all_names(object_array):
    for i in range(len(object_array)):
        print(str(i+1) + '.',object_array[i].username)

# Creating the database connection for the server
def create_database_connection():
    # Creating a connection object to connect with the database
    database_connector = psycopg2.connect(database = 'mtalkz', user = 'postgres', password = '123456',
                                            host = '127.0.0.1', port = 5432)
    return database_connector       # Returning the connector

# # Function for adding the client to the database of the server
# def add_client_to_the_database(username, type):
#     database_connector = create_database_connection()       # Getting connector object to connect with database
#     cursor = database_connector.cursor()
#     try:
#         # Executing the SQL command and inserting username and its type into the database
#         cursor.execute('INSERT INTO clients(username, type) VALUES(%s,%s)', (username,type))   
#         database_connector.commit()
#         database_connector.close()
#     except Exception as e:
#         print("Exception:", e)

def create_id():
    return str(int(time.time()*100000))

def get_field_agent_id(username):
    database_connector = create_database_connection()
    id = None
    if database_connector:
        try:
            cursor = database_connector.cursor()
            cursor.execute('SELECT id FROM field_agent_details where username = %s', (username,))
            id = cursor.fetchone()[0]
        except Exception as e:
            print('Exception:', e)
    return id


def get_customer_id(username):
    database_connector = create_database_connection()
    id = None
    if database_connector:
        try:
            cursor = database_connector.cursor()
            cursor.execute('SELECT id FROM customer_details where username = %s', (username,))
            id = cursor.fetchone()[0]
        except Exception as e:
            print('Exception:', e)
    return id

# Function for adding the messages and its details to the database
def add_message_to_the_database(values):
    database_connector = create_database_connection()
    cursor = database_connector.cursor()
    try:
        cursor.execute('INSERT INTO message_details VALUES(%s,%s,%s,%s,%s)',values)
        database_connector.commit()
        database_connector.close()
    except Exception as e:
        print('Exception:', e)

# Function to get the customer object
def get_customer_object(username, connection):
    customer_object = None
    for customer in customer_available:
        if customer.username == username and customer.connection == connection:
            customer_object = customer
            break
    return customer_object

# Function for handling the client
def handle_client(connection, address, username, type):
    while True:
        try:                                              
            msg_from_client_encoded = connection.recv(1024)              # Getting message from the client side in bits
            msg_from_client_decoded = msg_from_client_encoded.decode()   # Decoding the message into string
            print('Message from client : ', msg_from_client_decoded)
        except:
            """
                If Customer:- remove customer from customer_available list, connected_clients list.
                If Field Agent:- remove field agent from field_agent_available list, 
                                 make connected_field_agent to None.
            """
            print('No Message Recieved from client')
            return

        msg_id = create_id()
        timestamp = int(time.time())
        if type == 'field_agent':
            # send msg to corresponding connected customer having given username
            """
                msg_from_client_decoded for field agent will be in the form of "Username|Message". 
                So in order to get Username and Message seperately from msg_from_client_decode, we'll
                use split() function.
            """
            info_from_msg = msg_from_client_decoded.split(',')
            print(info_from_msg)
            customer_username, msg_for_customer = info_from_msg[0], info_from_msg[1]
            sender_id = get_field_agent_id(username); reciever_id = get_customer_id(customer_username) 
            values = (msg_id,sender_id,reciever_id,timestamp,msg_for_customer)
            # Adding the message send by the field agent to customer in database
            add_message_to_the_database(values)
            # Searching for the connection object of the customer with given username
            customer_connector = get_connection_object_for_customer(username,customer_username)
            if customer_connector is not None:
                """
                    After the getting connector of the customer, sending the message to the customer 
                    in appropiate format. 
                """

                send_message_to_customer(customer_connector,username,msg_for_customer)
        else:
            # send msg to corresponding connected field agent having given username
            """
                Here msg_from_client_decoded for customer will be in the form of normal string. So we can
                simply send to the corresponding field agent.
            """
            customer_object = get_customer_object(username, connection)
            field_agent_connector = get_connection_object_for_field_agent(username)
            sender_id = get_customer_id(username); 
            reciever_id = get_field_agent_id(customer_object.connected_field_agent.username)
            values = (msg_id,sender_id,reciever_id,timestamp,msg_from_client_decoded)
            add_message_to_the_database(values)
            if field_agent_connector is not None:
                send_message_to_field_agent(field_agent_connector,username,msg_from_client_decoded)

# Sending message to customer connected to corresponding field agent
def send_message_to_customer(customer_connector, username, msg_for_customer):
    # Creating the message in appropiate format
    msg_to_be_send = 'Message from Agent ' + username + ' : ' + msg_for_customer
    # Converting the message in bits
    msg_to_be_send_encoded = msg_to_be_send.encode()
    try:
        customer_connector.send(msg_to_be_send_encoded)     # Sending the message to the customer
    except Exception as e:
        print("Exception:",e)

# Sending message to field agent connected to corresponding to customer
def send_message_to_field_agent(field_agent_connector, username, msg_for_field_agent):
    # Creating the message in appropiate format
    msg_to_be_send = 'Message from Customer ' + username + ' : ' + msg_for_field_agent
    # Converting the message in bits
    msg_to_be_send_encoded = msg_to_be_send.encode()
    try:
        field_agent_connector.send(msg_to_be_send_encoded)  # Sending the message to the field agent
    except Exception as e:
        print('Exception:',e)

# Searching for the connection object of the customer
def get_connection_object_for_customer(username,customer_username):
    """
        Logic:
                Initially take connector object as None, so traverse through each field agent in the
                field_agent_available list. In each field agent, traverse through all customers connected to
                that field agent, check customer.username is equal to username or not, if yes change the value
                of the connector object and return it. 
    """
    customer_connector = None                            # Taking object as None initially
    for agent in field_agent_available:                  # Traversing through each agent in field_agent_available
        if agent.username == username:
            for customer in agent.connected_customers:       # Traversing through each customer in agent.connector_customers
                if customer.username == customer_username:   # If yes, change the value of connector
                    customer_connector = customer.connection
                    break
        if customer_connector is not None:
            break
    return customer_connector                            # Returning the connector_object

# Searching for the connection object of the field_customer
def get_connection_object_for_field_agent(username):
    """
        Logic:
                Initially take connector object as None, now traverse through each customer in customer_available
                list. Now check for each customer whether customer.username is equal or not, if yes change the value
                of the connector object to that connection object and return it.
    """
    field_agent_connector = None                        # Taking object as None initially
    for customer in customer_available:                 # Traversing through each agent in customer_available
        if customer.username == username:               # If yes, change the value of connector
            field_agent_connector = customer.connected_field_agent.connection
            break
    return field_agent_connector                        # Returning the connector_object

# Creating connection between the client and customer
def create_connection_btw_customer_n_field_agent():
    """
        Logic:-
                Here, we are checking for all the customers whether there's connected_field_agent is None or not. 
                If yes, we are searching for a field agent having least no of customers connected to it. After 
                finding that field agent, we are appending the customer into the list of connected_customer of the 
                field agent and initialising the field agent to connected_field_agent of the customer.
    """
    for customer_index in range(len(customer_available)):
        free_field_agent_index = None   # Initially assuming all the field agents has same no of customers
        # Connection only when the customer has no field agent connected to it
        if customer_available[customer_index].connected_field_agent is None:
            for field_agent_index in range(len(field_agent_available)):
                """
                    If free_field_index is None, it can assume that all the field agents have same no of customers
                    connected to them.
                """
                if ((free_field_agent_index is None) or 
                    (len(field_agent_available[free_field_agent_index].connected_customers) > 
                     len(field_agent_available[field_agent_index].connected_customers))):
                    free_field_agent_index = field_agent_index
            field_agent_available[free_field_agent_index].connected_customers.append(customer_available[customer_index])
            customer_available[customer_index].connected_field_agent = field_agent_available[free_field_agent_index]
            print(customer_available[customer_index].username + ' has been connected to ' + field_agent_available[free_field_agent_index].username)