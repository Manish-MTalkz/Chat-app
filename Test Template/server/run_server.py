from server_main import *
if __name__ == '__main__':
    try:
        start_server()
    except Exception as e:
        print(e)