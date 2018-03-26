from PyQt5 import QtWidgets

class Server(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent=None, id=None, name="", getNick=None, *args, **kwargs):
        super(Server, self).__init__(parent)
        self.name = name
        self.id = id
        self.setText(0, name)
        self.channels = []
        self.getNick = getNick
        
    def addChannel(self, channel):
        self.channels.append(channel)
        
    def selected(self, window):
        window.nickLabel.setText(self.getNick(self.id))