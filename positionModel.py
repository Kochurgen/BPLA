from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QAbstractListModel, QModelIndex, QVariant

class PositionModel(QAbstractListModel):
    def __init__(self, data=None):
        super().__init__()
        self._data = data or []


    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return QVariant()
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()]
        return QVariant()

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if index.isValid() and role==Qt.ItemDataRole.EditRole:
            self._data[index.row()] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def flags(self, index):
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable

    def insertRow(self, value, position=None):
        pos = position if position is not None else len(self._data)
        self.beginInsertRows(QModelIndex(), pos, pos)
        self._data.insert(pos, value)
        self.endInsertRows()

    def removeRow(self, row):
        if 0 <= row < len(self._data):
            self.beginRemoveRows(QModelIndex(), row, row)
            self._data.pop(row)
            self.endRemoveRows()