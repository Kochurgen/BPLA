from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIntValidator
from PyQt6.QtNetwork import QTcpSocket
import json


class Position(QtWidgets.QWidget):
    connectPosition = pyqtSignal(dict)
    changeBearingValue = pyqtSignal(dict)
    getPositionByLocation = pyqtSignal(bool)
    disconnectPosition = pyqtSignal(dict)
    updateData =  pyqtSignal(dict)

    def __init__(self, data, id, parent=None):
        super().__init__(parent)
        uic.loadUi("connect_block.ui", self)
        self._data = data
        self._id = id
        self.positionLabel.setText(f"Позиція № {id}")
        self.connectPushButton.clicked.connect(self.connectToPosition)
        self.disconnectPushButton.clicked.connect(self.disconnectFromPosition)
        self.disconnectPushButton.setVisible(False)
        self.pushButtonPlus.clicked.connect(self.incrementPlus)
        self.pushButtonMinus.clicked.connect(self.incrementMinus)
        self.settingsPushButton.clicked.connect(self.goToSettings)
        self.cancelPushButton.clicked.connect(self.goToPositionControl)
        self.savePushButton.clicked.connect(self.savePosition)
        self.dial.sliderReleased.connect(self.slider_relised)
        self.dial.valueChanged.connect(self.value_changed)
        self.client_socket = QTcpSocket()
        self.client_socket.connected.connect(self.on_connected)
        self.client_socket.disconnected.connect(self.on_disconnected)
        self.client_socket.readyRead.connect(self.read_data)
        self.client_socket.errorOccurred.connect(self.handle_error)
        self.activeStateElements(False)
        self.validator = QIntValidator(0, int(self._data.get('angle')))
        self.incrementSize.setValidator(self.validator)
        self.incrementSize.setValidator(self.validator)
        self.bearingLabel.setText(self._data.get('correction'))
        self.fillPositionData()


    def savePosition (self):
        print("hello")
        # self.data_sent.emit("Hello from Second Window!")
        ip = self.ipLineEdit.text()
        port = self.portLineEdit.text()
        correction = self.correctionLineEdit.text()
        angle = self.angleLineEdit.text()
        lat = self.latLineEdit.text()
        lng = self.lngLineEdit.text()
        # self.data_sent.emit({"ip": ip, "port": port, "correction": correction, "angle": angle, "lat": lat, "lng": lng})
        print(self._data)
        self._data = {"ip": ip, "port": port, "correction": correction, "angle": angle, "lat": lat, "lng": lng, "id": self._id}
        self.updateData.emit(self._data)

    def connectToPosition (self):
        self.client_socket.connectToHost(self._data.get('ip'), int(self._data.get('port')))
        # self.connectPosition.emit({"lat": self._data.get('lat'), "lng": self._data.get('lng'), "id": self._id,
        #                            "correction": self._data.get("correction")})
        # self.connectPushButton.setVisible(False)
        # self.disconnectPushButton.setVisible(True)
        # self.activeStateElements(True)

    def disconnectFromPosition (self):
        self.client_socket.disconnectFromHost()

    def value_changed(self, i):
        value = int(self._data.get('correction')) + i
        if value > 360:
            value = value - 360
        self.changeBearingValue.emit({"bearing": int(self._data.get('correction')) + i, "id": self._id})
        self.bearingLabel.setText(f"{value}")

    def slider_relised(self):
        message = f"{self.dial.value()}\n".encode()
        self.client_socket.write(message)

    def getPositionLocation(self):
        self.getPositionByLocation()

    def slider_position(self, p):
        print("position", p)
        # updateLineByBearing

    def on_connected(self):
        self.connectPosition.emit({"lat": self._data.get('lat'), "lng": self._data.get('lng'), "id": self._id,
                                   "correction": self._data.get("correction")})
        self.connectPushButton.setVisible(False)
        self.disconnectPushButton.setVisible(True)
        self.activeStateElements(True)

    def on_disconnected(self):
        print("disconected")
        self.disconnectPosition.emit({"id" : self._id})
        self.disconnectPushButton.setVisible(False)
        self.connectPushButton.setVisible(True)
        self.activeStateElements(False)

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

    def activeStateElements(self, status):
        self.dial.setEnabled(status)
        self.pushButtonPlus.setEnabled(status)
        self.pushButtonMinus.setEnabled(status)
        self.bearingLabel.setText(self._data.get('correction'))
        self.dial.setValue(0)

    def incrementPlus(self):
        if (int(self._data.get('angle'))+1) > int(self.incrementSize.text()):
            incr = int(self.dial.value()) + int(self.incrementSize.text())
            if incr < (int(self._data.get('angle'))+1):
                self.dial.setValue(incr)
                message = f"{self.dial.value()}\n".encode()
                self.client_socket.write(message)

    def incrementMinus(self):
        if (int(self._data.get('angle'))+1) > int(self.incrementSize.text()):
            incr = int(self.dial.value()) - int(self.incrementSize.text())
            if incr > -1:
                self.dial.setValue(incr)
                message = f"{self.dial.value()}\n".encode()
                self.client_socket.write(message)

    def goToSettings(self):
        self.stackedWidget.setCurrentIndex(1)

    def goToPositionControl(self):
        self.stackedWidget.setCurrentIndex(0)

    def fillPositionData(self):
        self.ipLineEdit.setText(self._data.get("ip"))
        self.portLineEdit.setText(self._data.get("port"))
        self.correctionLineEdit.setText(self._data.get("correction"))
        self.angleLineEdit.setText(self._data.get("angle"))
        self.latLineEdit.setText(self._data.get("lat"))
        self.lngLineEdit.setText(self._data.get("lng"))


