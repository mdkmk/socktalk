import sys
import socket
import threading
import errno
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal

class ReceiverThread(QThread):
    received_signal = pyqtSignal(str)

    def __init__(self, client_socket, header_length):
        super().__init__()
        self.client_socket = client_socket
        self.header_length = header_length
        self.running = True

    def run(self):
        while self.running:
            try:
                while True:
                    username_header = self.client_socket.recv(self.header_length)
                    if not len(username_header):
                        print("Connection closed by the server")
                        self.terminate()
                    username_length = int(username_header.decode("utf-8").strip())
                    username = self.client_socket.recv(username_length).decode("utf-8")
                    message_header = self.client_socket.recv(self.header_length)
                    message_length = int(message_header.decode("utf-8").strip())
                    message = self.client_socket.recv(message_length).decode("utf-8")

                    formatted_message = f"{username} > {message}"
                    self.received_signal.emit(formatted_message)
            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print("Reading error", str(e))
                    self.terminate()
                continue
            except Exception as e:
                print("General error", str(e))
                self.terminate()

    def stop(self):
        self.running = False
        self.terminate()

class ChatClient(QMainWindow):
    HEADER_LENGTH = 10

    def __init__(self, ip, port, username):
        super().__init__()
        self.ip = ip
        self.port = port
        self.username = username
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.ip, self.port))
        self.client_socket.setblocking(False)
        username_encoded = self.username.encode("utf-8")
        username_header = f"{len(username_encoded):<{self.HEADER_LENGTH}}".encode("utf-8")
        self.client_socket.send(username_header + username_encoded)
        self.initUI()
        self.receiver_thread = ReceiverThread(self.client_socket, self.HEADER_LENGTH)
        self.receiver_thread.received_signal.connect(self.update_text_area)
        self.receiver_thread.start()

    def initUI(self):
        self.setWindowTitle(f"{self.username}'s Chatty Client")
        self.setGeometry(100, 100, 400, 600)

        layout = QVBoxLayout()

        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)
        layout.addWidget(self.text_area)

        self.input_area = QLineEdit(self)
        self.input_area.setPlaceholderText(f"Message as {self.username}")
        layout.addWidget(self.input_area)

        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.write)
        layout.addWidget(self.send_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    @pyqtSlot()
    def write(self):
        message = self.input_area.text()
        self.send_message(message)
        # Display the message in the client's text display box
        self.update_text_area(f"{self.username} > {message}")
        self.input_area.clear()

    def send_message(self, message):
        if message:
            message_encoded = message.encode("utf-8")
            message_header = f"{len(message_encoded):<{self.HEADER_LENGTH}}".encode("utf-8")
            self.client_socket.send(message_header + message_encoded)

    @pyqtSlot(str)
    def update_text_area(self, message):
        self.text_area.append(message)

    def closeEvent(self, event):
        self.receiver_thread.stop()
        self.client_socket.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    username = input("Enter your username: ")
    client = ChatClient("127.0.0.1", 1234, username)
    client.show()
    sys.exit(app.exec_())
