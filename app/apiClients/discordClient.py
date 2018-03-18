import logging
import discord
import asyncio
from app.app import FusionChat
from app.server import Server
from app.channel import Channel
from app.message import Message

class DiscordClient(discord.Client):
    
    def __init__(self, signaler=None, *args, **kwargs):
        super(DiscordClient, self).__init__(*args, **kwargs)
        self.signaler = signaler
        self.servers = []
        
    async def connectDiscord(self, loop):
        await asyncio.ensure_future(self.login(FusionChat.settings.getSettings()['discord'], bot=False))
        loop.create_task(self.connect())

    async def on_ready(self):
        logging.info('Logged into Discord as ' + self.user.name + '(' + str(self.user.id) + ')')
        self._populateServerTree()
            
    def _populateServerTree(self):
        for server in self.guilds:
            qServer = Server(name=server.name)
            for channel in server.channels:
                if channel.__class__.__name__ == "CategoryChannel":
                    qChannel = Channel(parent=qServer, name=channel.name, id=channel.id)
                    qServer.addChannel(qChannel)
            for channel in server.channels:
                if channel.__class__.__name__ == "TextChannel":
                    sendFunc = lambda m, c=channel:self.sendMessage(c, m)
                    foundCategory = False
                    for category in qServer.channels:
                        if channel.category_id == category.id:
                            qChannel = Channel(parent=category, name=channel.name, id=channel.id, sendMessage=sendFunc)
                            category.subchannels.append(qChannel)
                            foundCategory = True
                    if not foundCategory:
                        qChannel = Channel(parent=qServer, name=channel.name, id=channel.id, sendMessage=sendFunc)
                        qServer.addChannel(qChannel)
                elif channel.__class__.__name__ == "VoiceChannel":
                    continue
                elif channel.__class__.__name__ == "CategoryChannel":
                    continue
                else:
                    logging.error("channel type not handled: " + channel.__class__.__name__)
            self.signaler.addServer.emit(qServer)
            self.servers.append(qServer)
        
    async def on_message(self, message):
        logging.debug('message received: ' + message.content)
        for server in self.servers:
            for channel in server.channels:
                self._findMessageDestination(message, channel)
        #self.signaler.updateText.emit(message.content)
        
    def _findMessageDestination(self, message, channel):
        if message.channel.id == channel.id:
            sender = message.author.nick
            if sender == None:
                sender = message.author.name
            messageObj = Message(sender=sender, text=message.content, timeStamp=message.created_at)
            self.signaler.addMessage.emit(channel, messageObj)
        for subchannel in channel.subchannels:
            self._findMessageDestination(message, subchannel)
            
    def sendMessage(self, channel, message):
        #channel.send(content=message)
        logging.debug('sent message: ' + message)