from PyQt5 import QtCore
import fusionchat.server
import fusionchat.channel
import fusionchat.message

class QtSignaler(QtCore.QObject):
    addServer = QtCore.pyqtSignal(fusionchat.server.Server)
    addMessage = QtCore.pyqtSignal(fusionchat.channel.Channel, fusionchat.message.Message)
    
    def __init__(self):
        super(QtSignaler, self).__init__()
        