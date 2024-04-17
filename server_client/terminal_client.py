import socket
import sys
import threading
import errno

class ReceiverThread(threading.Thread):
    def __init__(self, client_socket, header_length, username):
        super().__init__()
        self.client_socket = client_socket
        self.header_length = header_length
        self.username = username
        self.running = True

    def run(self):
        while self.running:
            try:
                while True:
                    message_header = self.client_socket.recv(self.header_length)
                    if not len(message_header):
                        if self.running:
                            print("\nConnection closed by the server")
                        self.running = False
                        return
                    message_length = int(message_header.decode("utf-8").strip())
                    message = self.client_socket.recv(message_length).decode("utf-8")
                    print("\r" + message + f"\n{self.username} > ", end="")
                    sys.stdout.flush()
            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print("\nReading error", str(e))
                    self.running = False
                    return
                continue
            except Exception as e:
                print("\nGeneral error", str(e))
                self.running = False
                return

    def stop(self):
        self.running = False
        self.join()

def main(server_ip, server_port):
    HEADER_LENGTH = 10
    username = input("Enter your username: ")
    server_port = int(server_port)
    print("Chat client is running...")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    client_socket.setblocking(False)

    username_encoded = username.encode("utf-8")
    username_header = f"{len(username_encoded):<{HEADER_LENGTH}}".encode("utf-8")
    client_socket.send(username_header + username_encoded)

    receiver_thread = ReceiverThread(client_socket, HEADER_LENGTH, username)
    receiver_thread.start()

    try:
        while True:
            message = input(f"{username} > ")
            if message:
                message_encoded = message.encode("utf-8")
                message_header = f"{len(message_encoded):<{HEADER_LENGTH}}".encode("utf-8")
                client_socket.send(message_header + message_encoded)
    except KeyboardInterrupt:
        print("\nShutting down...")
        receiver_thread.stop()

if __name__ == '__main__':
    server_ip = input("Enter server IP (for default 127.0.0.1, press enter): ") or "127.0.0.1"
    server_port = input("Enter server port (for default 1234, press enter): ") or "1234"
    main(server_ip, server_port)
