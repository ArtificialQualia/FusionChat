import logging
import discord
import asyncio
from app.app import FusionChat
import app.server
import app.channel
import app.message

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
        for server in self.guilds:
            serverObject = app.server.Server(server.name)
            for channel in server.channels:
                if channel.__class__.__name__ == "CategoryChannel":
                    channelObject = app.channel.Channel(name=channel.name, id=channel.id)
                    serverObject.addChannel(channelObject)
            for channel in server.channels:
                if channel.__class__.__name__ == "TextChannel":
                    foundCategory = False
                    for category in serverObject.channels:
                        if channel.category_id == category.id:
                            channelObject = app.channel.Channel(name=channel.name, id=channel.id)
                            category.subchannels.append(channelObject)
                            foundCategory = True
                    if not foundCategory:
                        channelObject = app.channel.Channel(name=channel.name, id=channel.id)
                        serverObject.addChannel(channelObject)
                elif channel.__class__.__name__ == "VoiceChannel":
                    continue
                elif channel.__class__.__name__ == "CategoryChannel":
                    pass
                else:
                    logging.error("channel type not handled: " + channel.__class__.__name__)
            self.signaler.addServer.emit(serverObject)
            self.servers.append(serverObject)
        
    async def on_message(self, message):
        print(message.content)
        for server in self.servers:
            for channel in server.channels:
                self._findMessageDestination(message, channel)
        self.signaler.updateText.emit(message.content)
        
    def _findMessageDestination(self, message, channel):
        if message.channel.id == channel.id:
            messageObj = app.message.Message(sender=message.author.nick, text=message.content, timeStamp=message.created_at)
            channel.addMessage(messageObj)
        for subchannel in channel.subchannels:
            self._findMessageDestination(message, subchannel)