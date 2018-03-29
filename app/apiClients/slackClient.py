import logging
import slackclient
from app.server import Server
from app.channel import Channel
from app.message import Message

class SlackClient(slackclient.SlackClient):
    
    def __init__(self, signaler=None, token=None, *args, **kwargs):
        super(SlackClient, self).__init__(token, *args, **kwargs)
        self.signaler = signaler
        self.servers = []
        self.token = token
        
        authTestResponse = self.api_call("auth.test")
        if not authTestResponse['ok']:
            logigng.error('Problem with Slack token: ' + str(authTestResponse['error']))
            return
        self.userName = authTestResponse['user']
        self.userId = authTestResponse['user_id']
        self.teamName = authTestResponse['team']
        self.teamId = authTestResponse['team_id']
        logging.info('Logged into Slack Workspace "' + self.teamName + '" as ' + self.userName + ' (' + str(self.userId) + ')')
        self._populateServerTree()
        
    def getNick(self, serverID):
        return self.userName
            
    def _populateServerTree(self):
        channels = self.api_call("channels.list")['channels']
        topLevelName = "Slack (" + self.teamName + ")"
        qTopLevelServer = Server(name=topLevelName, id=self.teamId, getNick=self.getNick)
        for channel in channels:
            if channel['is_member']:
                qChannel = Channel(parent=qTopLevelServer, name=channel['name'], id=channel['id'])
                qTopLevelServer.addChannel(qChannel)
        self.signaler.addServer.emit(qTopLevelServer)
        
    def _findMessageDestination(self, message, channel):
        pass
            
    def sendMessage(self, channel, message):
        pass