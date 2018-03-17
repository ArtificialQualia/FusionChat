from PyQt5 import QtWidgets, QtCore
import app.gui.mainWindow as mainWindow
import app.gui.addServer as addServerDialog
import threading
import app.server
import app.channel
import app.settingsHandler

class FusionChat(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow, QtCore.QObject):
    
    settings = app.settingsHandler.SettingsHandler()
    
    def __init__(self, parent=None, client=None, signaler=None):
        super(FusionChat, self).__init__(parent)
        self.setupUi(self)
        self.plainTextEdit.appendPlainText("test")
        self.signaler = signaler
        self.signaler.updateText.connect(self.writeMessage)
        self.signaler.addServer.connect(self.addServer)
        self.actionAddServer.triggered.connect(self.showServerDialog)
        
        self.serverLine.mouseMoveEvent = self.dragServerLine
        
    def dragServerLine(self, event):
        if (self.serverTree.maximumWidth() != self.serverTree.width()):
            self.serverTree.setMaximumWidth(self.serverTree.width())
        self.serverTree.setMaximumWidth(self.serverTree.maximumWidth() + event.x())
        
    def writeMessage(self, message):
        self.plainTextEdit.appendPlainText(message)
        
    def showServerDialog(self):
        dialog = AddServerDialog()
        dialog.exec()
        
    def addServer(self, server):
        qServer = QtWidgets.QTreeWidgetItem(self.serverTree)
        for channel in server.channels:
            qChannel = QtWidgets.QTreeWidgetItem(qServer)
            qChannel.setText(0, channel.name)
            qServer.addChild(qChannel)
            qChannel.setExpanded(True)
            for subchannel in channel.subchannels:
                qSubchannel = QtWidgets.QTreeWidgetItem(qChannel)
                qSubchannel.setText(0, subchannel.name)
                qChannel.addChild(qSubchannel)
                qSubchannel.setExpanded(True)
        qServer.setText(0, server.name)
        qServer.setExpanded(True)
        self.serverTree.addTopLevelItem(qServer)
        
class AddServerDialog(QtWidgets.QDialog, addServerDialog.Ui_Dialog):
    def __init__(self, parent=None):
        super(AddServerDialog, self).__init__(parent)
        self.setupUi(self)
    
    def accept(self):
        FusionChat.settings.setSettings(discord=self.tokenInput.text())
        QtWidgets.QDialog.accept(self)