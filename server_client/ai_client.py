import os
import socket
import time
import openai
import errno
import sys

class AIChatClient:
    HEADER_LENGTH = 10

    def __init__(self, ip, port, username, mode, interval):
        self.ip = ip
        self.port = port
        self.username = username
        self.mode = mode
        self.interval = interval
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.ip, self.port))
        self.client_socket.setblocking(False)
        self.send_username()
        self.line_count = 0
        self.last_response_time = time.time()
        self.openai_client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.error_reported = False

    def send_username(self):
        username_encoded = self.username.encode("utf-8")
        username_header = f"{len(username_encoded):<{self.HEADER_LENGTH}}".encode("utf-8")
        self.client_socket.send(username_header + username_encoded)

    def receive_message(self):
        while True:
            try:
                while True:
                    message_header = self.client_socket.recv(self.HEADER_LENGTH)
                    if not len(message_header):
                        print("Connection closed by the server")
                        sys.exit()
                    message_length = int(message_header.decode("utf-8").strip())
                    message = self.client_socket.recv(message_length).decode("utf-8")
                    self.handle_message(message)
            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print("Reading error:", str(e))
                    break
                continue
            except Exception as e:
                print("Error receiving message:", str(e))
                break

    def handle_message(self, message):
        username, _, content = message.partition(' > ')
        if username.strip() != self.username:
            if self.mode == 1:
                self.line_count += 1
                if self.line_count >= self.interval:
                    self.respond_to_message(content)
                    self.line_count = 0
            elif self.mode == 2:
                if time.time() - self.last_response_time >= self.interval:
                    self.respond_with_new_message()
                    self.last_response_time = time.time()

    def handle_error(self, error_message):
        if not self.error_reported:
            print(error_message)
            self.send_message(error_message)
            self.error_reported = True

    def respond_to_message(self, message):
        try:
            chat_completion = self.openai_client.chat.completions.create(
                messages=[
                    {"role": "user", "content": message}
                ],
                model="gpt-3.5-turbo",
            )
            response_text = chat_completion.choices[0].message["content"].strip()
            self.send_message(response_text)
        except Exception as e:
            self.handle_error(f"Error calling OpenAI API: {e}")

    def respond_with_new_message(self):
        try:
            chat_completion = self.openai_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Start a new conversation."},
                    {"role": "user", "content": "Say something interesting."}
                ],
                model="gpt-3.5-turbo",
            )
            response_text = chat_completion.choices[0].message["content"].strip()
            self.send_message(response_text)
        except Exception as e:
            self.handle_error(f"Error calling OpenAI API: {e}")

    def send_message(self, message):
        message_encoded = message.encode("utf-8")
        message_header = f"{len(message_encoded):<{self.HEADER_LENGTH}}".encode("utf-8")
        self.client_socket.send(message_header + message_encoded)
