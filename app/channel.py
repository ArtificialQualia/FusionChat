class Channel(object):
    def __init__(self, name="", id="", *args, **kwargs):
        self.name = name
        self.messages = []
        self.subchannels = []
        self.id = id
        
    def addMessage(self, message):
        self.messages.append(message)