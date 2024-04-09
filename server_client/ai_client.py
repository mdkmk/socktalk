import os
import socket
import time
import openai
import errno


class AIChatClient:
    HEADER_LENGTH = 10

    def __init__(self, server, ip, port, username, mode1_enabled, mode1_interval, mode2_enabled, mode2_interval, send_full_chat_history):
        self.ip = ip
        self.port = port
        self.username = username
        self.mode1_enabled = mode1_enabled
        self.mode1_interval = mode1_interval
        self.mode2_enabled = mode2_enabled
        self.mode2_interval = mode2_interval
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.ip, self.port))
        self.client_socket.setblocking(False)
        self.send_username()
        self.line_count = 0
        self.last_response_time = float('inf')
        self.openai_client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.error_reported = False
        self.conversation_history = []
        self.send_full_chat_history = send_full_chat_history
        self.running = True
        self.server = server

    def shutdown(self):
        self.running = False
        try:
            self.client_socket.close()
        except Exception as e:
            print(f"Error closing socket: {e}")

    def send_username(self):
        username_encoded = self.username.encode("utf-8")
        username_header = f"{len(username_encoded):<{self.HEADER_LENGTH}}".encode("utf-8")
        self.client_socket.send(username_header + username_encoded)

    def receive_message(self):
        while self.running:
            try:
                if self.mode2_enabled and self.server.get_user_client_count() > 0:
                    if self.last_response_time == float('inf'):
                        self.last_response_time = time.time()
                    elif time.time() - self.last_response_time >= self.mode2_interval:
                        self.respond_with_new_message()
                        self.last_response_time = time.time()
                elif self.mode2_enabled and self.server.get_user_client_count() == 0:
                    self.last_response_time = float('inf')

                message_header = self.client_socket.recv(self.HEADER_LENGTH)
                if not len(message_header):
                    print("Connection closed by the server")
                    break
                message_length = int(message_header.decode("utf-8").strip())
                message = self.client_socket.recv(message_length).decode("utf-8")
                self.handle_message(message)

            except IOError as e:
                if e.errno == errno.EBADF:
                    print("Client socket closed, stopping receive loop")
                    break
                elif e.errno not in (errno.EAGAIN, errno.EWOULDBLOCK):
                    print(f"Reading error: {e}")
                    break

            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def handle_message(self, message):
        username, _, content = message.partition(' > ')
        if username.strip() != self.username:
            self.conversation_history.append({"role": "user", "content": content})
            if self.mode1_enabled:
                self.line_count += 1
                if self.line_count >= self.mode1_interval:
                    self.respond_to_message()
                    self.line_count = 0

    def handle_error(self, error_message):
        if not self.error_reported:
            print(error_message)
            self.send_message(error_message)
            self.error_reported = True

    def respond_to_message(self):
        try:
            messages_to_send = self.conversation_history if self.send_full_chat_history else self.conversation_history[-self.mode1_interval:]
            print("Sending messages to OpenAI:", messages_to_send)
            chat_completion = self.openai_client.chat.completions.create(
                messages=messages_to_send,
                model="gpt-3.5-turbo",
            )
            response_text = chat_completion.choices[0].message.content
            self.send_message(response_text)
            self.conversation_history.append({"role": "assistant", "content": response_text})
        except Exception as e:
            self.handle_error(f"Error calling OpenAI API: {e}")

    def respond_with_new_message(self):
        try:
            chat_completion = self.openai_client.chat.completions.create(
                messages=[
                    {"role": "user", "content": "Say something interesting from a random Wikipedia page,"
                                                " and start your response with 'Did you know', but don't mention"
                                                " the source."}
                ],
                model="gpt-3.5-turbo",
            )
            response_text = chat_completion.choices[0].message.content
            self.conversation_history.append({"role": "system", "content": response_text})
            self.send_message(response_text)
        except Exception as e:
            self.handle_error(f"Error calling OpenAI API: {e}")

    def send_message(self, message):
        message_encoded = message.encode("utf-8")
        message_header = f"{len(message_encoded):<{self.HEADER_LENGTH}}".encode("utf-8")
        self.client_socket.send(message_header + message_encoded)
