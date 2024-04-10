import sys
import socket
import errno
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QKeySequence


class ReceiverThread(QThread):
    received_signal = pyqtSignal(str)
    connection_closed_signal = pyqtSignal()

    def __init__(self, client_socket, header_length):
        super().__init__()
        self.client_socket = client_socket
        self.header_length = header_length
        self.running = True
        self.last_username = None

    def run(self):
        while self.running:
            try:
                while True:
                    message_header = self.client_socket.recv(self.header_length)
                    if not len(message_header):
                        if self.running:
                            print("Connection closed by the server")
                        self.running = False
                        self.connection_closed_signal.emit()
                        self.terminate()
                        return
                    message_length = int(message_header.decode("utf-8").strip())
                    message = self.client_socket.recv(message_length).decode("utf-8")
                    self.received_signal.emit(message)
            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print("Reading error", str(e))
                    self.running = False
                    self.terminate()
                    return
                continue
            except Exception as e:
                print("General error", str(e))
                self.running = False
                self.terminate()
                return

    def stop(self):
        self.running = False
        self.wait()


class CustomTextEdit(QTextEdit):
    def __init__(self, parent=None, chat_client=None):
        super().__init__(parent)
        self.chat_client = chat_client
        self.setFixedHeight(90)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if event.modifiers() & Qt.ShiftModifier:
                self.insertPlainText("\n")
            else:
                if self.chat_client:
                    self.chat_client.write()
        elif event.matches(QKeySequence.Paste):
            clipboard_text = QApplication.clipboard().text()
            self.insertPlainText(clipboard_text)
        else:
            super().keyPressEvent(event)


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
        self.send_username()
        self.initUI()
        self.receiver_thread = ReceiverThread(self.client_socket, self.HEADER_LENGTH)
        self.receiver_thread.received_signal.connect(self.update_text_area)
        self.receiver_thread.connection_closed_signal.connect(self.on_connection_closed)
        self.receiver_thread.start()

    def send_username(self):
        username_encoded = self.username.encode("utf-8")
        username_header = f"{len(username_encoded):<{self.HEADER_LENGTH}}".encode("utf-8")
        self.client_socket.send(username_header + username_encoded)

    def initUI(self):
        self.setWindowTitle(f"{self.username}'s Chat Client")
        self.setGeometry(100, 100, 400, 600)
        layout = QVBoxLayout()
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)
        layout.addWidget(self.text_area)
        self.input_area = CustomTextEdit(self, chat_client=self)
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
        message = self.input_area.toPlainText()
        self.send_message(message)
        self.update_text_area(f"{self.username} > {message}")
        self.input_area.clear()

    def send_message(self, message):
        message_encoded = message.encode("utf-8")
        message_header = f"{len(message_encoded):<{self.HEADER_LENGTH}}".encode("utf-8")
        self.client_socket.send(message_header + message_encoded)

    @pyqtSlot(str)
    def update_text_area(self, message):
        username, _, _ = message.partition(' > ')
        if self.receiver_thread.last_username and (username != self.receiver_thread.last_username or
                                                   ("AI" in username and "AI" in self.receiver_thread.last_username)):
            self.text_area.append("")
        self.text_area.append(message.replace('\n', '<br>'))
        self.receiver_thread.last_username = username

    def on_connection_closed(self):
        self.close()

    def closeEvent(self, event):
        if self.receiver_thread.isRunning():
            self.receiver_thread.stop()
            self.client_socket.close()
        event.accept()

def main():
    app = QApplication(sys.argv)
    username = input("Enter your username: ")
    server_ip = input("Enter server IP (for default 127.0.0.1, press enter): ") or "127.0.0.1"
    server_port = input("Enter server port (for default 1234, press enter): ") or "1234"
    server_port = int(server_port)
    client = ChatClient(server_ip, server_port, username)
    print("Chat client is running...")
    client.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    username = input("Enter your username: ")
    client = ChatClient("127.0.0.1", 1234, username)
    client.show()
    sys.exit(app.exec_())
