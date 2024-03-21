import threading
import time
import os
from server import ChatServer
from ai_client import AIChatClient

def start_server(ip, port):
    server = ChatServer(ip, port)
    server.run()

def start_ai_client(ip, port):
    os.environ["OPENAI_API_KEY"] = "<open ai api key here>"


    username = "AI"
    mode = 1
    interval = 3

    ai_client = AIChatClient(ip, port, username, mode, interval)

    receive_thread = threading.Thread(target=ai_client.receive_message)
    receive_thread.start()


if __name__ == '__main__':
    ip_address = "127.0.0.1"
    port = 1234

    server_thread = threading.Thread(target=start_server, args=(ip_address, port))
    server_thread.start()

    time.sleep(5)

    start_ai_client(ip_address, port)

    server_thread.join()
