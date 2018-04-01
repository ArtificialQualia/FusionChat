import logging
import irc.client
import sys
from app.server import Server
from app.channel import Channel
from app.message import Message

class IrcClient():
    
    def __init__(self, signaler=None, *args, **kwargs):
        self.signaler = signaler
        self.servers = []
        self.server = kwargs['server']
        self.port = kwargs['port']
        self.ssl = kwargs['ssl']
        self.nick = kwargs['nick']
        self.password = kwargs['password']
        
        reactor = irc.client.Reactor()
        try:
            self.client = reactor.server().connect(self.server, self.port, self.nick)
        except irc.client.ServerConnectionError:
            logging.error(sys.exc_info()[1])
            logging.error("Failed to join " + self.server)
            return
        self.client.add_global_handler("welcome", self.on_connect)
        self.client.add_global_handler("join", self.on_join)
        self.client.add_global_handler("disconnect", self.on_disconnect)
        reactor.process_forever()
        
    def getNick(self, serverID):
        return self.client.get_nickname()
    
    def on_connect(self, connection, event):
        self._populateServerTree()
        self.client.join("#help")
            
    def _populateServerTree(self):
        topLevelName = "IRC (" + self.server + ")"
        self.qTopLevelServer = Server(name=topLevelName, id=self.server, getNick=self.getNick)
        self.signaler.addServer.emit(self.qTopLevelServer)
        
    def on_join(self, connection, event):
        print(event)
        qChannel = Channel(parent=self.qTopLevelServer, name=str(event.target), id=str(event.target))
    
    def on_disconnect(self, connection, event):
        logging.info("Disconnected from " + event.source + ", reason: " + event.arguments[0])
        #remove from tree
        
    def _findMessageDestination(self, message, channel):
        pass
            
    def sendMessage(self, channel, message):
        pass