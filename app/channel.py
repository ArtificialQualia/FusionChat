class Channel(object):
    def __init__(self, name="", *args, **kwargs):
        self.name = name
        self.messages = []
        
    def addMessage(self, message):
        self.messages.append(message)