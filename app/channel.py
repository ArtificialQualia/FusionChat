from PyQt5 import QtWidgets, QtGui

class Channel(QtWidgets.QTreeWidgetItem):
    redBrush = QtGui.QBrush(QtGui.QColor('red'))
    blackBrush = QtGui.QBrush(QtGui.QColor('black'))
    
    def __init__(self, parent=None, name="", id="", sendMessage=None, *args, **kwargs):
        super(Channel, self).__init__(parent)
        self.parent = parent
        self.name = name
        self.setText(0, name)
        self.messages = []
        self.subchannels = []
        self.id = id
        self.sendMessage = sendMessage
        
    def addMessage(self, messageDisplay, message):
        self.messages.append(message)
        if self.isSelected():
            self.displayMessage(messageDisplay, message)
        else:
            self.setForeground(0, self.redBrush)
            
    def selected(self, window):
        if self.isSelected():
            self.setForeground(0, self.blackBrush)
            window.messageDisplay.clear()
            for message in self.messages:
                self.displayMessage(window.messageDisplay, message)
        self.parent.selected(window)
            
    def displayMessage(self, messageDisplay, message):
        messageFixedLines = message.text.replace("\n", "</p><p>")
        messageDisplay.append("<p>" + "[" + message.timeStamp.isoformat() + "] <b>" + message.sender + "</b>: " + messageFixedLines + "</p>")