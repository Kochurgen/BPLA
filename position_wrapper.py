from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIntValidator
from PyQt6.QtNetwork import QTcpSocket
import json

class Position (QtWidgets.QWidget):
    data_update = pyqtSignal(dict)
    toggleGetCoordinate = pyqtSignal(bool)

    def __init__(self, data, id, parent=None):
        super().__init__(parent)
        uic.loadUi("connect_block.ui", self)
        self.savePushButton.clicked.connect(self.savePosition)
        self.ipLineEdit.setValidator(ipValidator(self.ipLineEdit))
        self.lngLineEdit.setValidator(longitudeValidator(self.lngLineEdit))
        self.latLineEdit.setValidator(latitudeValidator(self.latLineEdit))
        self.locationPushButton.clicked.connect(self.getCoordinate)
        self.id = id

    def getCoordinate(self):
        # self.toggleGetCoordinate.emit(False)
        self.GetCoordinates = not self.GetCoordinates
        self.toggleGetCoordinate.emit(self.GetCoordinates)

    def setResponse(self, data):
        print("📩 PositionSettings отримав:", data.get("lat"))
        if self.GetCoordinates:
            self.latLineEdit.setText(str(data.get("lat")))
            self.lngLineEdit.setText(str(data.get("lng")))
            self.GetCoordinates = not self.GetCoordinates

    def savePosition (self):
        ip = self.ipLineEdit.text()
        port = self.portLineEdit.text()
        correction = self.correctionLineEdit.text()
        angle = self.angleLineEdit.text()
        lat = self.latLineEdit.text()
        lng = self.lngLineEdit.text()
        self.data_update.emit({"ip": ip, "port": port, "correction": correction, "angle": angle, "lat": lat, "lng": lng, "id": self.id})