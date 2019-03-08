import slackclient
import time
import html
import datetime
from fusionchat.server import Server
from fusionchat.channel import Channel
from fusionchat.message import Message

import logging
logger = logging.getLogger(__name__)

class SlackClient(slackclient.SlackClient):
    
    def __init__(self, signaler=None, token=None, *args, **kwargs):
        super(SlackClient, self).__init__(token)
        self.signaler = signaler
        self.servers = []
        self.token = token
        
        authTestResponse = self.api_call("auth.test")
        if not authTestResponse['ok']:
            logger.error('Problem with Slack token: ' + str(authTestResponse['error']))
            return
        self.userName = authTestResponse['user']
        self.userId = authTestResponse['user_id']
        self.teamName = authTestResponse['team']
        self.teamId = authTestResponse['team_id']
        logger.info('Logged into Slack Workspace "' + self.teamName + '" as ' + self.userName + ' (' + str(self.userId) + ')')
        self._populateServerTree()
        self._RTMLoop()
        
    def _RTMLoop(self):
        if self.rtm_connect(with_team_state=False):
            while True:
                for event in self.rtm_read():
                    self._handleSlackEvent(event)
                time.sleep(1)
            else:
                logger.error('Slack RTM Connection Failed for "' + self.teamName + '" as ' + self.userName + ' (' + str(self.userId) + ')')

    def getNick(self, serverID):
        return self.userName
            
    def _handleSlackEvent(self, event):
        eventType = event.get('type')
        if eventType == 'hello':
            pass
        elif eventType == 'message':
            self._handleSlackMessage(event)
        else:
            logger.info('Unhandled Slack Event: ' + str(event))

    def _handleSlackMessage(self, event):
        for channel in self.qTopLevelServer.channels:
            if event['channel'] == channel.id:
                logger.debug('message recieved: ' + event['text'])
                htmlSafeMessage = html.escape(event['text'])
                messageTime = datetime.datetime.fromtimestamp(float(event['ts']))
                messageObj = Message(sender=event['user'], text=htmlSafeMessage, timeStamp=messageTime)
                self.signaler.addMessage.emit(channel, messageObj)
                return
        logger.error('No channel found for message: ' + str(event))

    def _populateServerTree(self):
        channels = self.api_call("channels.list")['channels']
        topLevelName = "Slack (" + self.teamName + ")"
        self.qTopLevelServer = Server(name=topLevelName, id=self.teamId, getNick=self.getNick)
        for channel in channels:
            if channel['is_member']:
                qChannel = Channel(parent=self.qTopLevelServer, name=channel['name'], id=channel['id'])
                self.qTopLevelServer.addChannel(qChannel)
        self.signaler.addServer.emit(self.qTopLevelServer)
            
    def sendMessage(self, channel, message):
        pass