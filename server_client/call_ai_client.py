import os
import threading
from ai_client import AIChatClient

if __name__ == '__main__':
    os.environ["OPENAI_API_KEY"] = "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"

    ip_address = "127.0.0.1"
    port = 1234

    username = "AI"
    mode = 1
    interval = 3

    ai_client = AIChatClient(ip_address, port, username, mode, interval)

    receive_thread = threading.Thread(target=ai_client.receive_message)
    receive_thread.start()

    receive_thread.join()