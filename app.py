import sys
import json
from sys import exception

from PyQt6 import QtCore, QtGui, QtWidgets, QtWebChannel
from PyQt6 import uic
from PyQt6.QtCore import QUrl, Qt, QObject, pyqtSignal
from PyQt6.QtWebEngineWidgets import QWebEngineView
from position import Position
from position_settings import PositionSettings

class AnotherWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)

class Backend(QtCore.QObject):
    dataProcessed = QtCore.pyqtSignal(dict)

    @QtCore.pyqtSlot(str, result=str)
    def process_data_from_js(self, js_data_str):
        # Process the data received from JavaScript
        py_obj = json.loads(js_data_str)
        print("Received from JS:", py_obj)
        # Optionally, send a response back to JavaScript
        # response_data = {"status": "success", "processed_value": py_obj["value"] * 2}
        self.dataProcessed.emit(py_obj)
        # return json.dumps(response_data)


class Bridge(QObject):
    domEventReceived = pyqtSignal(str)

    def receiveMessage(self, msg):
        print("Отримано з DOM:", msg.value)
        # self.domEventReceived.emit(msg)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("MapPage.ui", self)
        self.browser = QWebEngineView()
        self.verticalLayoutMap.addWidget(self.browser)
        self.pushButtonAddMarker.clicked.connect(self.showPositionSettings)
        self.pushButtonSetCenter.clicked.connect(self.setCenter)
        self._data = []
        self.backend = Backend()
        self.backend.dataProcessed.connect(self.receiveResponse)
        self.content_widget = QtWidgets.QWidget()
        self.scrollArea.setWidget(self.content_widget)
        self.channel = QtWebChannel.QWebChannel()
        self.channel.registerObject("backend", self.backend)
        self.browser.page().setWebChannel(self.channel)
        self.scrollArea.setWidgetResizable(True)
        self.layout = QtWidgets.QVBoxLayout(self.content_widget)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        for i in self._data:
            _position = Position()
            self.layout.addWidget(_position)
        self.content_widget.setLayout(self.layout)
        self.browser.setUrl(QUrl("http://localhost:8080/map.html"))
        # self.connectPosition.connect(self.addMarker)

    def removeMarker(self, id):
        print("RemoveMarker")
        print(id)
        self.browser.page().runJavaScript(str("removeMarker({})".format(id.get("id"))))

    def setMarker(self, latLng):
        print('setMarker')
        self.browser.page().runJavaScript(str("addMarker({}, {})".format(latLng.get("lng"), latLng.get("lat"))))
        #self.browser.page().runJavaScript(str("addMarker({}, {})".format(self.lat_2, self.lng_2)))

    def setLine(self, data):
        self.browser.page().runJavaScript(str("addLine({}, {}, {}, {})".format(data.get("lng"), data.get("lat"), data.get("correction"), data.get("id"))))

    def removeLine(self, data):
        self.browser.page().runJavaScript(str("removeLine({})".format(data.get("id"))))

    def setCenter(self):
        self.browser.page().runJavaScript(str("setCenter({}, {})".format(self.lat, self.lng)))

    def showPositionSettings(self, chenged):
        self.w = PositionSettings()
        self.w.data_sent.connect(self.addPosition)
        self.w.toggleGetCoordinate.connect(self.getCoordinates)
        self.w.show()

    def addPosition(self, data):
        self._data.append(data)
        _position = Position(data, len(self._data))
        self.layout.addWidget(_position)
        _position.connectPosition.connect(self.setLine)
        _position.changeBearingValue.connect(self.updateBearing)
        _position.updateData.connect(self.updatePosition)
        _position.disconnectPosition.connect(self.removeLine)

        self.setMarker({"lat": data.get('lat'), "lng": data.get('lng')})
        if len(self._data)>2:
            self.pushButtonAddMarker.setEnabled(False)
        if self.w:  # Check if the window exists
            self.w.close()
            self.w = None

    def updatePosition(self, data: dict):
        self._data[int(data.get('id')-1)] = data


    def getCoordinates(self):
        print("getCoordinates")
        # self.browser.page().runJavaScript(
        #     str("updateLineByBearing({}, {})".format(data.get("bearing"), data.get("id"))))

    def removePosition(self, index):
        self._data.pop(index)

    def connectPositionSuccess(self):
        self.window.connectPosition.connect(self.setMarker)

    def updateBearing(self, data):
        self.browser.page().runJavaScript(str("updateLineByBearing({}, {})".format(data.get("bearing"), data.get("id"))))

    def receiveResponse(self, data: dict):
        print("⚡ Отримано response_data:", data)
        if getattr(self, "w", None) is not None:
            self.w.setResponse(data)



app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

