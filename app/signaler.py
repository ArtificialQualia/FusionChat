from PyQt5 import QtCore
import app.server
import app.channel
import app.message

class QtSignaler(QtCore.QObject):
    updateText = QtCore.pyqtSignal(str)
    addServer = QtCore.pyqtSignal(app.server.Server)
    addMessage = QtCore.pyqtSignal(app.channel.Channel, app.message.Message)
    
    def __init__(self):
        super(QtSignaler, self).__init__()
        