class Server(object):
    def __init__(self, name="", *args, **kwargs):
        self.name = name
        self.channels = []
        
    def addChannel(self, channel):
        self.channels.append(channel)
        
