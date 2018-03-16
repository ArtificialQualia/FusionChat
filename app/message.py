class Message(object):
    def __init__(self, sender="", text="", timeStamp="", *args, **kwargs):
        self.sender = sender
        self.text = text
        self.timeStamp = timeStamp