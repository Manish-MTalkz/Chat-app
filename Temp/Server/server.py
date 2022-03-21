# IMPORTING THE LIBRARIES
import socket
import threading

FIELD_AGENTS = [] # All the field agents available on the server
CUSTOMERS = [] # All the customers available on the server

FIELD_AGENT_ID = 1 # ID's for all the field agents
CUSTOMER_ID = 1 # ID's for all the customers

class FIELD_AGENT:
    def __init__(self, username, conn):
        self.username = username
        self.conn = conn
        global FIELD_AGENT_ID
        self.id = FIELD_AGENT_ID
        FIELD_AGENT_ID += 1
        self.__customer_connections = []
        self.__is_active = True

    def total_connections(self):
        return len(self.__customer_connections)

    def add_customer(self, customer):
        self.__customer_connections.append(customer)

class CUSTOMER:
    def __init__(self, username, conn):
        self.username = username
        self.conn = conn
        global CUSTOMER_ID
        self.id = CUSTOMER_ID
        CUSTOMER_ID += 1
        self.__agent_connection = None

    def is_connected(self):
        return self.__agent_connection != None

    def connect_agent(self, agent):
        self.agent_connection = agent

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname(socket.gethostbyname())
    port = int(input('Enter port to run the server on --> '))
    s.bind((host,port))
    s.listen(100)
    print('Running on host: ', host)
    print('Running on port: ', port)

    while True:
        conn, addr = s.accept()
        msg_from_client = conn.recv(1024).decode()
        client_handler = threading.Thread(target = handle_clients, args = (conn, addr, msg_from_client))
        client_handler.start()

def handle_clients(conn, addr, msg_from_client):
    dtype, username = msg_from_client.split()[0], msg_from_client.split()[1]
    if dtype == 'FIELD_AGENT':
        field_agent = FIELD_AGENT(username, conn)
        FIELD_AGENTS.append(field_agent)
    else:
        customer = CUSTOMER(username, conn)
        CUSTOMERS.append(customer)
    create_connections()
    while True:
        try:
            msg = conn.recv(1024).decode()
        except:
            conn.shutdown(socket.SHUT_RDWR)
            if dtype == 'FIELD_AGENT':
                pass
            else:
                pass
            break
        if dtype == 'FIELD_AGENT' and msg != '':
            pass
        elif msg != '':
            pass

def create_connections():
    field_index = 0
    for index in range(len(FIELD_AGENTS)):
        if FIELD_AGENTS[index].total_connections < FIELD_AGENTS[field_index].total_connections:
            field_index = index
    for index in range(len(CUSTOMERS)):
        if CUSTOMERS[index].is_connected is False:
            CUSTOMERS[index].connect_agent(FIELD_AGENTS[field_index])
            FIELD_AGENT[field_index].add_customer(CUSTOMERS[index])
            break