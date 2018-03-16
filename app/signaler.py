from PyQt5 import QtCore

class QtSignaler(QtCore.QObject):
    updateText = QtCore.pyqtSignal(str)
    addServer = QtCore.pyqtSignal(str)