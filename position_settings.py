from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from Validator import ipValidator, latitudeValidator, longitudeValidator


class PositionSettings(QtWidgets.QWidget):
    data_sent = pyqtSignal(dict)
    toggleGetCoordinate = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("addPosition.ui", self)
        self.GetCoordinates = False
        self.savePositionPushButton.clicked.connect(self.savePosition)
        self.ipLineEdit.setValidator(ipValidator(self.ipLineEdit))
        self.lngLineEdit.setValidator(longitudeValidator(self.lngLineEdit))
        self.latLineEdit.setValidator(latitudeValidator(self.latLineEdit))
        self.locationPushButton.clicked.connect(self.getCoordinate)

    def getCoordinate (self):
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
        self.data_sent.emit({"ip": ip, "port": port, "correction": correction, "angle": angle, "lat": lat, "lng": lng})
        # print(ip, port, correction, angle, lat, lng)
