#<------------------------------------- Class for Customer and Field Agent ----------------------------------------->#

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

class message:
    def __init__(self, id, sender_id, reciever_id, time, msg):
        self.id = id                        # Saving id of the msg in the database
        self.sender_id = sender_id          # Saving the id of the user who sent the message
        self.reciever_id = reciever_id      # Saving the id of the user who recieved the message
        self.time = time                    # Saving time at which message is recieved
        self.msg = msg                      # Saving the message send by the user