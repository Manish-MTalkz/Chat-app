from client_libraries import *
FIELD_AGENTS = [] # Keeping the records of the FIELD AGENTS connected to the server.
CUSTOMERS = [] # Keeping the record for the CUSTOMERS connected to the server.

# Searching for the Agent for the available Field Agents
def search(username,password):
    for agent in FIELD_AGENTS:
        if agent.user_name == username and agent.password == password:
            return agent
    return None

# Searching for the Agent using id with the help of binary search
def searchByID(id):
    start = 0; end = len(FIELD_AGENTS)-1
    while start <= end:
        mid = start+(end-start)//2
        if FIELD_AGENTS[mid].id == id:
            return mid
        elif FIELD_AGENTS[mid].id < id:
            start = mid+1
        else:
            end = mid-1
    return -1

# Creating connection with the server with the help of the socket library
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def create_connection(client):
    while True:
        try:
            host = input('Enter the host name --> ')
            port = int(input('Enter the port no --> '))
            s.connect((host,port))
            break
        except:
            print('Could not connect the server, please try again.')
            exit()
    s.send((str(client.type) + ' ' + str(client.user_name)).encode())
    message_handler = threading.Thread(target = handle_message, args = ())
    message_handler.start()
    input_handler = threading.Thread(target = handle_input, args = ())
    input_handler.start()

# Recieving the messages from the server
def handle_message():
    while True:
        print(s.recv(1024).decode())

# Send the messages to the server
def handle_input():
    while True:
        s.send(input().encode())