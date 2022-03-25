# Creating the class for the customer for all its features and handle its functionality
class customer:
    def __init__(self, username, connection):
        self.username = username            # Initialising username of the customer with the given username
        self.connection = connection        # Saving the connection object of customer to get and recieve messages
        self.type = 'customer'              # Saving the type of the client
        self.connected_field_agent = None   # Field agent connected to this customer 

# Creating the class for the field_agent for all its features and handle its functionality
class field_agent:
    def __init__(self, username, connection):
        self.username = username            # Initialising username of the field agent with given username 
        self.connection = connection        # Saving the connection object of field agent to get and recieve messages
        self.type = 'field_agent'           # Saving the type of the client
        self.connected_customers = []       # All customers connected to this field agent