# Importing the Libraries
import socket    # socket library is for creating sockets of client and server, connecting with each other
import threading # threading library is for creating threads of the various functions in the server and client
import psycopg2  # psycopg2 library is for creating the connection between the client and database for the authentication
from client_object import * # Importing all the classes definede in client_object 
import time                 # Importing time library for creating id for the msg, client and user