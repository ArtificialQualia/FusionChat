import discord
import asyncio

class DiscordClient(discord.Client):
    
    def __init__(self, signaler=None, *args, **kwargs):
        super(DiscordClient, self).__init__(*args, **kwargs)
        self.signaler = signaler
        
    async def connectDiscord(self, loop):
        await asyncio.ensure_future(self.login("", bot=False))
        print('before of connect')
        loop.create_task(self.connect())
        print('end of connect')

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        print('adding servers to sidebar')
        for server in self.servers:
            self.signaler.addServer.emit(server.name)
        
    async def on_message(self, message):
        print(message.content)
        self.signaler.updateText.emit(message.content)