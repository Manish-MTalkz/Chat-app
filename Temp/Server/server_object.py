FIELD_AGENT_ID = 1 # ID's for all the field agents
CUSTOMER_ID = 1 # ID's for all the customers

class FIELD_AGENT:
    def __init__(self, username, conn):
        self.username = username
        self.conn = conn
        global FIELD_AGENT_ID
        self.id = FIELD_AGENT_ID
        FIELD_AGENT_ID += 1
        self.customer_connections = []
        self.is_active = True

    def total_connections(self):
        return len(self.customer_connections)

    def add_customer(self, customer):
        self.customer_connections.append(customer)

    def send_msg_to_customer(self, username, msg):
        for customer in self.customer_connections:
            if customer.username == username:
                connection = customer.conn
                connection.send(msg)
                break

class CUSTOMER:
    def __init__(self, username, conn):
        self.username = username
        self.conn = conn
        global CUSTOMER_ID
        self.id = CUSTOMER_ID
        CUSTOMER_ID += 1
        self.agent_connection = None

    def is_connected(self):
        return self.agent_connection != None

    def connect_agent(self, agent):
        self.agent_connection = agent

    def send_msg_to_agent(self, username, msg):
        self.agent_connection.conn.send(msg.encode())