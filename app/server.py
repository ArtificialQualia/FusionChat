from PyQt5 import QtWidgets

class Server(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent=None, name="", *args, **kwargs):
        super(Server, self).__init__(parent)
        self.name = name
        self.setText(0, name)
        self.channels = []
        
    def addChannel(self, channel):
        self.channels.append(channel)
        
    def selected(self, messageDisplay):
        pass