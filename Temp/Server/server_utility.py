from server_libraries import *

FIELD_AGENTS = [] # All the field agents available on the server
CUSTOMERS = [] # All the customers available on the server

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostbyname(socket.gethostname())
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
            msg_recieved = conn.recv(1024).decode()
        except:
            conn.shutdown(socket.SHUT_RDWR)
            if dtype == 'FIELD_AGENT':
                pass
            else:
                pass
            break
        if dtype == 'FIELD_AGENT' and msg_recieved != '':
            customer_username, msg_for_customer = msg_recieved[0], msg_recieved[1]
            current_agent = None
            for agent in FIELD_AGENTS:
                if agent.conn == conn:
                    current_agent = agent
                    break
            if not current_agent:
                for customer in current_agent.customer_connections:
                    if customer.username == customer_username:
                        customer.conn.send(msg_for_customer.encode())
        elif msg_recieved != '':
            field_username, msg_for_agent = msg_recieved[0], msg_recieved[1]
            for customer in CUSTOMERS:
                if customer.agent_connection.username == field_username:
                    customer.agent_connection.send(msg_for_agent.encode())

def create_connections():
    field_index = 0
    for index in range(len(FIELD_AGENTS)):
        if (FIELD_AGENTS[index].total_connections() < FIELD_AGENTS[field_index].total_connections() 
            and FIELD_AGENTS[index].is_active is True):
            field_index = index
    for index in range(len(CUSTOMERS)):
        if CUSTOMERS[index].is_connected() is False:
            CUSTOMERS[index].connect_agent(FIELD_AGENTS[field_index])
            FIELD_AGENTS[field_index].add_customer(CUSTOMERS[index])
            break