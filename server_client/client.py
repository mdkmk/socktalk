import socket
import select
import errno
import sys
import threading

class ChatClient:
    HEADER_LENGTH = 10

    def __init__(self, ip, port, username):
        self.ip = ip
        self.port = port
        self.username = username
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.ip, self.port))
        self.client_socket.setblocking(False)
        username_encoded = self.username.encode("utf-8")
        username_header = f"{len(username_encoded):<{self.HEADER_LENGTH}}".encode("utf-8")
        self.client_socket.send(username_header + username_encoded)

    def send_message(self):
        while True:
            message = input(f"{self.username} > ")
            if message:
                message_encoded = message.encode("utf-8")
                message_header = f"{len(message_encoded):<{self.HEADER_LENGTH}}".encode("utf-8")
                self.client_socket.send(message_header + message_encoded)

    def receive_message(self):
        last_username = None
        while True:
            try:
                while True:
                    username_header = self.client_socket.recv(self.HEADER_LENGTH)
                    if not len(username_header):
                        print("Connection closed by the server")
                        sys.exit()
                    username_length = int(username_header.decode("utf-8").strip())
                    username = self.client_socket.recv(username_length).decode("utf-8")
                    message_header = self.client_socket.recv(self.HEADER_LENGTH)
                    message_length = int(message_header.decode("utf-8").strip())
                    message = self.client_socket.recv(message_length).decode("utf-8")
                    if username != last_username:
                        print(f"{username} > ", end="")
                    print(message)
                    last_username = username
            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print("Reading error", str(e))
                    sys.exit()
                continue
            except Exception as e:
                print("General error", str(e))
                sys.exit()

    def run(self):
        send_thread = threading.Thread(target=self.send_message)
        receive_thread = threading.Thread(target=self.receive_message)
        send_thread.start()
        receive_thread.start()
        send_thread.join()
        receive_thread.join()

if __name__ == "__main__":
    username = input("Username: ")
    client = ChatClient("127.0.0.1", 1234, username)
    client.run()