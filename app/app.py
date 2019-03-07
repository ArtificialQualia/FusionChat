import sys
from threading import Thread
import asyncio
from PyQt5 import QtWidgets, QtCore
import app.gui.mainWindow as mainWindow
import app.gui.addServer as addServerDialog
import app.server
import app.channel
from app.settingsHandler import settings
from app.apiClients import *

class FusionChat(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow, QtCore.QObject):
    
    styleSheet = "p { margin-top: 0px; margin-bottom: 0px; margin-right: 0px; margin-left:0px; } \
    body {margin-top: 1px; margin-bottom: 1px; margin-right: 1px; margin-left:1px; }"
    
    def __init__(self, parent=None, signaler=None):
        super(FusionChat, self).__init__(parent)
        self.setupUi(self)
        self.messageDisplay.document().setDocumentMargin(0)
        self.messageDisplay.document().setDefaultStyleSheet(self.styleSheet)
        self.signaler = signaler
        self.signaler.addServer.connect(self.addServer)
        self.actionAddServer.triggered.connect(self.showServerDialog)
        self.serverTree.itemSelectionChanged.connect(self.serverTreeSelectionChanged)
        self.signaler.addMessage.connect(lambda c, m:c.addMessage(self.messageDisplay, m))
        
        self.messageInput.keyPressEvent = self.keyPressMessageInput
        self.serverLine.mouseMoveEvent = self.dragServerLine
        
        for auth in settings.getSettings()['auth']:
            apiModule = getattr(sys.modules[__name__], auth['apiModuleName'])
            apiClass = getattr(apiModule, auth['apiClassName'])
            t = Thread(target=lambda: apiClass(signaler=signaler, **auth), daemon=True)
            t.start()
        
    def dragServerLine(self, event):
        if (self.serverTree.maximumWidth() != self.serverTree.width()):
            self.serverTree.setMaximumWidth(self.serverTree.width())
        self.serverTree.setMaximumWidth(self.serverTree.maximumWidth() + event.x())
        
    def showServerDialog(self):
        dialog = AddServerDialog()
        dialog.exec()
        
    def addServer(self, server):
        self.serverTree.addTopLevelItem(server)
        self.serverTree.expandAll()
        
    def serverTreeSelectionChanged(self):
        try:
            self.serverTree.selectedItems()[0].selected(self)
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
        settings.setSettings(discord=self.tokenInput.text())
        QtWidgets.QDialog.accept(self)