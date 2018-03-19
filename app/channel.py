from PyQt5 import QtWidgets, QtGui

class Channel(QtWidgets.QTreeWidgetItem):
    redBrush = QtGui.QBrush(QtGui.QColor('red'))
    blackBrush = QtGui.QBrush(QtGui.QColor('black'))
    
    def __init__(self, parent=None, name="", id="", sendMessage=lambda:print('no sendmessage handler for this channel'), *args, **kwargs):
        super(Channel, self).__init__(parent)
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
            
    def selected(self, messageDisplay):
        self.setForeground(0, self.blackBrush)
        messageDisplay.clear()
        for message in self.messages:
            self.displayMessage(messageDisplay, message)
            
    def displayMessage(self, messageDisplay, message):
        marginText = "margin-top: 0px; margin-bottom: 0px; margin-right: 0px; margin-left:20px;"
        indentedParagraph = "<p style=\" "+marginText+" text-indent:-20px;\">"
        messageFixedLines = message.text.replace("\n", "</p><p style=\" "+marginText+" text-indent:-10px;\">")
        messageDisplay.append(indentedParagraph + "[" + message.timeStamp.isoformat() + "] <b>" + message.sender + "</b>: " + messageFixedLines + "</p>")