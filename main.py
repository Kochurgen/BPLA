import sys

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic
from PyQt6.QtNetwork import QTcpSocket

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("main.ui", self)
        self.lineEdit_ip.textChanged.connect(self.on_ip_text_changed)
        self.lineEdit_port.textChanged.connect(self.on_port_text_changed)
        self.dial.valueChanged.connect(self.on_dial_value_changed)
        self.pushButton_connect.clicked.connect(self.the_button_was_clicked)
        self.client_socket = QTcpSocket()
        self.client_socket.connected.connect(self.on_connected)
        self.client_socket.disconnected.connect(self.on_disconnected)
        self.client_socket.readyRead.connect(self.read_data)
        self.client_socket.errorOccurred.connect(self.handle_error)

    def on_connected(self):
        print("conected")

    def on_disconnected(self):
        print("disconected")

    def read_data(self):
        data = self.client_socket.readAll().data()
        print(f"Received from server: {data.decode()}")

    def handle_error(self):
        print("handle_error")

    def on_ip_text_changed(self, text):
        self.server_address = text

    def on_port_text_changed(self, text):
        self.server_port = int(text)

    def on_dial_value_changed(self, value):
        message = f"{value}\n".encode()
        self.client_socket.write(message)

    def the_button_was_clicked(self):
        self.client_socket.connectToHost(self.server_address, self.server_port)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
