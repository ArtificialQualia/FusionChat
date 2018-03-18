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
        self.serverTree.itemSelectionChanged.connect(self.serverTreeSelectionChanged)
        self.signaler.addMessage.connect(lambda c, m:c.addMessage(self.plainTextEdit, m))
        
        self.messageInput.keyPressEvent = self.keyPressMessageInput
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
        self.serverTree.addTopLevelItem(server)
        self.serverTree.expandAll()
        
    def serverTreeSelectionChanged(self):
        try:
            self.serverTree.selectedItems()[0].selected(self.plainTextEdit)
        except IndexError:
            pass
        
    def keyPressMessageInput(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Return : 
            try:
                selectedChannel = self.serverTree.selectedItems()[0]
                selectedChannel.sendMessage(self.messageInput.toPlainText())
                self.messageInput.clear()
            except IndexError:
                pass
        else:
            QtWidgets.QPlainTextEdit.keyPressEvent(self.messageInput, event)
        
class AddServerDialog(QtWidgets.QDialog, addServerDialog.Ui_Dialog):
    def __init__(self, parent=None):
        super(AddServerDialog, self).__init__(parent)
        self.setupUi(self)
    
    def accept(self):
        FusionChat.settings.setSettings(discord=self.tokenInput.text())
        QtWidgets.QDialog.accept(self)