import socket
import select

class ChatServer:
    HEADER_LENGTH = 10

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen()
        self.sockets_list = [self.server_socket]
        self.clients = {}
        self.running = True


    def receive_message(self, client_socket):
        try:
            message_header = client_socket.recv(self.HEADER_LENGTH)
            if not len(message_header):
                return False
            message_length = int(message_header.decode("utf-8").strip())
            return {"header": message_header, "data": client_socket.recv(message_length)}
        except:
            return False

    def run(self):
        while self.running:
            try:
                read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list)
                for notified_socket in read_sockets:
                    if notified_socket == self.server_socket:
                        client_socket, client_address = self.server_socket.accept()
                        user = self.receive_message(client_socket)
                        if user is False:
                            continue
                        self.sockets_list.append(client_socket)
                        self.clients[client_socket] = user
                        print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")
                    else:
                        message = self.receive_message(notified_socket)
                        if message is False:
                            print(f"Closed connection from {self.clients[notified_socket]['data'].decode('utf-8')}")
                            self.sockets_list.remove(notified_socket)
                            del self.clients[notified_socket]
                            continue
                        user = self.clients[notified_socket]
                        print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
                        for client_socket in self.clients:
                            if client_socket != notified_socket:
                                combined_message = user['data'] + b' > ' + message['data']
                                combined_header = f"{len(combined_message):<{self.HEADER_LENGTH}}".encode("utf-8")
                                client_socket.send(combined_header + combined_message)

                for notified_socket in exception_sockets:
                    self.sockets_list.remove(notified_socket)
                    del self.clients[notified_socket]
            except OSError as e:
                if self.running:
                    print(f"Server accept error: {e}")
                else:
                    print("Server socket closed")
                    break
            except Exception as e:
                print(f"Unexpected error: {e}")

    def shutdown(self):
        self.running = False
        self.server_socket.close()


if __name__ == "__main__":
    server = ChatServer("127.0.0.1", 1234)
    server.run()
