#<------------------------------------- Classes for Customer and Field Agent ---------------------------------------->#

# Creating a class customer for all its features and functionalities
class customer:
    def __init__(self, id, email, username):
        self.id = id
        self.email = email
        self.username = username
        self.type = 'customer'
        self.active = True

# Creating a class field_agent for all its features and functionalities
class field_agent:
    def __init__(self, id, email, username, password):
        self.id = id
        self.email = email
        self.username = username
        self.type = 'field_agent'
        self.active = True
        self.password = password