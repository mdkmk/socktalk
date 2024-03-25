import threading
import time
import os
from server_v4 import ChatServer
from ai_client_v5 import AIChatClient

def start_server(ip, port):
    server = ChatServer(ip, port)
    server.run()


def start_ai_client(ip, port, mode1_active, mode1_interval, mode2_active, mode2_interval):

    if mode1_active:
        username_mode1 = "AI_mode1"
        ai_client_mode1 = AIChatClient(ip, port, username_mode1, mode=1, interval=mode1_interval)
        receive_thread_mode1 = threading.Thread(target=ai_client_mode1.receive_message)
        receive_thread_mode1.start()

    if mode2_active:
        username_mode2 = "AI_mode2"
        ai_client_mode2 = AIChatClient(ip, port, username_mode2, mode=2, interval=mode2_interval)
        receive_thread_mode2 = threading.Thread(target=ai_client_mode2.receive_message)
        receive_thread_mode2.start()

def main(server_ip_address, server_port, ai_mode1_active, ai_mode1_interval, ai_mode2_active, ai_mode2_interval):
    server = ChatServer(server_ip_address, server_port)
    server_thread = threading.Thread(target=server.run)
    server_thread.start()

    time.sleep(1)

    start_ai_client(server_ip_address, server_port, ai_mode1_active, ai_mode1_interval, ai_mode2_active, ai_mode2_interval)

    server_thread.join()


if __name__ == '__main__':
    server_ip_address = "127.0.0.1"
    server_port = 1234

    os.environ['OPENAI_API_KEY'] = "<API KEY HERE>"
    ai_mode1_active = True
    ai_mode1_interval = 3
    ai_mode2_active = False
    ai_mode2_interval = 20

    main(server_ip_address, server_port, ai_mode1_active, ai_mode1_interval, ai_mode2_active, ai_mode2_interval)


