#<------------------------------------- Classes for Customer and Field Agent ---------------------------------------->#
# Creating a class customer for all its features and functionalities
class customer:
    def __init__(self, username):
        self.username = username
        self.type = 'customer'

# Creating a class field_agent for all its features and functionalities
class field_agent:
    def __init__(self, username):
        self.username = username
        self.type = 'field_agent'