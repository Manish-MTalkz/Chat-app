# Class for the Field Agent and its properties
field_agent_count = 1 # To keep the count of the total field agents on the server
class FIELD_AGENT:
    def __init__(self):
        self.__new_field_agent()

    def __new_field_agent(self):
        self.user_name = input('Enter the User Name of Field Agent: ')
        self.password = input('Enter the Password: ')
        self.is_available = True
        self.type = 'FIELD_AGENT'
        global field_agent_count
        self.id = field_agent_count
        field_agent_count += 1
        print('You have been registered as the field agent on the server.')

# Class for the Customer and its properties
customer_count = 1 # To keep the count for the total customers on the server
class CUSTOMER:
    def __init__(self):
        self.__new_customer()

    def __new_customer(self):
        self.user_name = input('Enter the User Name of the Customer: ')
        self.type = 'CUSTOMER'
        global customer_count
        self.id = customer_count
        customer_count += 1