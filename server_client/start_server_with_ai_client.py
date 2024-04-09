import threading
import time
import os
from server import ChatServer
from ai_client import AIChatClient


def load_env_variables(filename='.env'):
    try:
        with open(filename) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    except FileNotFoundError:
        pass

    if os.environ.get("OPENAI_API_KEY") == "<OPENAI API KEY HERE>":
        print("Warning: OPENAI_API_KEY is not set. Please set the key or create an .env file")


def start_server(ip, port):
    server = ChatServer(ip, port)
    server.run()


def main(server_ip_address, server_port, send_full_chat_history, ai_mode1_active, ai_mode1_interval, ai_mode2_active, ai_mode2_interval):
    server = ChatServer(server_ip_address, server_port)
    server_thread = threading.Thread(target=server.run)
    server_thread.start()

    time.sleep(1)

    if ai_mode1_active or ai_mode2_active:
        username = "AI"
        ai_client = AIChatClient(server, server_ip_address, server_port, username, ai_mode1_active, ai_mode1_interval, ai_mode2_active, ai_mode2_interval, send_full_chat_history)
        threading.Thread(target=ai_client.receive_message).start()

    try:
        server_thread.join()
    except KeyboardInterrupt:
        print("Shutting down server and AI clients...")
        server.shutdown()
        if ai_client:
            ai_client.shutdown()
        server_thread.join()


if __name__ == '__main__':
    server_ip_address = "127.0.0.1"
    server_port = 1234

    os.environ['OPENAI_API_KEY'] = "<OPENAI API KEY HERE>"
    send_full_chat_history = True
    ai_mode1_active = True
    ai_mode1_interval = 1
    ai_mode2_active = True
    ai_mode2_interval = 60

    load_env_variables()
    main(server_ip_address, server_port, send_full_chat_history, ai_mode1_active, ai_mode1_interval, ai_mode2_active, ai_mode2_interval)
