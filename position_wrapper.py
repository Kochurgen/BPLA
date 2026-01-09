from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIntValidator
from PyQt6.QtNetwork import QTcpSocket
import json

class Position (QtWidgets.QWidget):
    def __init__(self, data, id, parent=None):
        super().__init__(parent)
        uic.loadUi("connect_block.ui", self)