from PyQt5 import QtWidgets
import app.gui.mainWindow as mainWindow

class ExampleApp(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow):
    def __init__(self, parent=None, client=None, signaler=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.plainTextEdit.appendPlainText("test")
        self.plainTextEdit.appendPlainText("test")
        self.plainTextEdit.appendPlainText("test")
        self.signaler = signaler
        self.signaler.updateText.connect(self.writeMessage)
        self.signaler.addServer.connect(self.addServer)
        
        self.serverLine.mouseMoveEvent = self.dragServerLine
        
    def dragServerLine(self, event):
        if (self.serverTree.maximumWidth() != self.serverTree.width()):
            self.serverTree.setMaximumWidth(self.serverTree.width())
        self.serverTree.setMaximumWidth(self.serverTree.maximumWidth() + event.x())
        
    def writeMessage(self, message):
        self.plainTextEdit.appendPlainText(message)
        
    def addServer(self, serverName):
        serverItem = QtWidgets.QTreeWidgetItem(self.serverTree)
        serverItem.setText(0, serverName)
        self.serverTree.addTopLevelItem(serverItem)
        
class ServerWidgetItem(QtWidgets.QTreeWidgetItem):
    pass