from client_utility import *

# Menu for the Field Agent
def menu_for_field_agent():
    print('1. Do you want to login ?')
    print('2. Do you want to sign up as a new agent?')
    choice = int(input('Please enter the choice: '))
    email = input('Please enter email: ')
    username = input('Please enter the username: ')
    password = input('Please enter the password: ')
    if choice == 1:
        login(email,username,password)
    elif choice == 2:
        new_field_agent = create_field_agent_object(email,username,password)  # Creating the instance of field_agent
        save_to_the_database(new_field_agent) # Saving username and password to the database for future authentication
        """
            After creating the instance of the customer, we are sending the request to the server to 
            accept the client as a field agent.
        """
        create_connection_to_the_server(new_field_agent)
    else:
        print('Wrong choice entered. Please try it again.')

""" 
    display() function is for creating the menu for the client whether 
    the client is customer or the field agent.
"""
def display():
    print('<----- Main Menu ----->')
    print('1. Customer')
    print('2. Field Agent')
    designation = int(input('Please enter the choice: '))

    if designation == 1:                            # All the functions related to the customer
        new_customer = create_customer_object()     # Instance of the customer class
        """
            After creating the instance of the customer, we are sending the request to the server to 
            accept the client as a customer.
        """
        save_to_the_database(new_customer)
        create_connection_to_the_server(new_customer)
    elif designation == 2:
        menu_for_field_agent()
    else:
        print('Wrong Designation Entered. Please try it again.')