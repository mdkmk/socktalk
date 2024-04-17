import threading
import time
import os
from server_client.server import ChatServer
from server_client.ai_client import AIChatClient


def start_server(ip, port):
    server = ChatServer(ip, port)
    server.run()


def main(server_ip="127.0.0.1", server_port=1234, send_full_chat_history=True, ai_mode1_active=True,
         ai_mode1_interval=1, ai_mode1_model="gpt-3.5-turbo", ai_mode2_active=True, ai_mode2_interval=60,
         ai_mode2_model="gpt-3.5-turbo", ai_mode2_content="Say something interesting from a random Wikipedia page and"
                                                       " start your response with 'Did you know', but don't mention the"
                                                       " source."):

    server = ChatServer(server_ip, server_port)
    server_thread = threading.Thread(target=server.run)
    server_thread.start()
    print("AI chat server is running...")
    time.sleep(1)

    if ai_mode1_active or ai_mode2_active:
        username = "AI"
        ai_client = AIChatClient(server, server_ip, server_port, username, ai_mode1_active, ai_mode1_interval,
                                 ai_mode1_model, ai_mode2_active, ai_mode2_interval, ai_mode2_model,
                                 send_full_chat_history, ai_mode2_content)
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
    server_ip = "127.0.0.1"
    server_port = 1234

    os.environ['OPENAI_API_KEY'] = "<OPENAI_API_KEY_HERE>"
    send_full_chat_history = True
    ai_mode1_active = True
    ai_mode1_interval = 1
    ai_mode1_model = "gpt-3.5-turbo"
    ai_mode2_active = True
    ai_mode2_interval = 60
    ai_mode2_model = "gpt-3.5-turbo"
    ai_mode2_content= ("Say something interesting from a random Wikipedia page and start your response with"
                       " 'Did you know', but don't mention the source.")

    main(server_ip, server_port, send_full_chat_history, ai_mode1_active, ai_mode1_interval, ai_mode1_model,
         ai_mode2_active, ai_mode2_interval, ai_mode2_model, ai_mode2_content)