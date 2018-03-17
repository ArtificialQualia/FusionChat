from PyQt5 import QtCore
import app.server

class QtSignaler(QtCore.QObject):
    updateText = QtCore.pyqtSignal(str)
    addServer = QtCore.pyqtSignal(app.server.Server)