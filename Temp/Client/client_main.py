from client_utility import *

def run():
    print('1. Customer')
    print('2. Field Agent')
    designation = int(input('Enter the designation: '))
    if designation == 1:
        customer = CUSTOMER()
        CUSTOMERS.append(customer)
        create_connection(customer)
    else:
        print('1. Login')
        print('2. New User')
        choice = int(input('Enter the choice: '))
        if choice == 1:
            while True:
                username = input('Enter the username: ')
                password = input('Enter the password: ')
                field_agent = search(username,password)
                FIELD_AGENTS[field_agent.id].is_available = True
                if field_agent:
                    try:
                        create_connection(field_agent)
                    except:
                        index = searchByID(field_agent.id)
                        if index != -1:
                            FIELD_AGENTS[index].is_available = False
                        print(f'{field_agent.user_name} is not available')
                        break
                else:
                    print(f'Field Agent with username -> {username} not found, please try again.')
        else:
            field_agent = FIELD_AGENT()
            FIELD_AGENTS.append(field_agent)
            create_connection(field_agent)
        exit() 