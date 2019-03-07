import logging
import discord
import asyncio
import html
#import app.app
from app.server import Server
from app.channel import Channel
from app.message import Message

class DiscordClient(discord.Client):
    
    def __init__(self, signaler=None, token=None, *args, **kwargs):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        super(DiscordClient, self).__init__()
        self.signaler = signaler
        self.servers = []
        self.token = token
        
        asyncio.ensure_future(self.connectDiscord(self.loop))
        self.loop.run_forever()
        
    async def connectDiscord(self, loop):
        await asyncio.ensure_future(self.login(self.token, bot=False))
        loop.create_task(self.connect())

    async def on_ready(self):
        logging.info('Logged into Discord as ' + self.user.name + ' (' + str(self.user.id) + ')')
        self._populateServerTree()
        
    def getNick(self, guildID):
        for server in self.guilds:
            if server.id == guildID:
                return server.me.nick if server.me.nick != None else server.me.name
        return self.user.name
            
    def _populateServerTree(self):
        topLevelName = "Discord (" + self.user.name + ")"
        qTopLevelServer = Server(name=topLevelName, id=0, getNick=self.getNick)
        for server in self.guilds:
            qServer = Server(parent=qTopLevelServer, name=server.name, id=server.id, getNick=self.getNick)
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
            self.servers.append(qServer)
        self.signaler.addServer.emit(qTopLevelServer)
        
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
            htmlSafeMessage = html.escape(message.content)
            messageObj = Message(sender=sender, text=htmlSafeMessage, timeStamp=message.created_at)
            self.signaler.addMessage.emit(channel, messageObj)
        for subchannel in channel.subchannels:
            self._findMessageDestination(message, subchannel)
            
    def sendMessage(self, channel, message):
        future = asyncio.run_coroutine_threadsafe(channel.send(content=message), self.loop)
        #need to handle rate limiting
        logging.debug('sent message: ' + message)