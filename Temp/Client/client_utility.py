from client_libraries import*

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