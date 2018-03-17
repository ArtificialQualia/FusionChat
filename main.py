import logging
import sys

import asyncio
from threading import Thread
from PyQt5 import QtWidgets

from app import app
from app.signaler import QtSignaler
from app.apiClients import discordClient

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    signaler = QtSignaler()
    appx = QtWidgets.QApplication(sys.argv)
    testDiscordClient = discordClient.DiscordClient(signaler=signaler)
    form = app.FusionChat(signaler=signaler, client=testDiscordClient)
    
    
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(testDiscordClient.connectDiscord(loop))
    t = Thread(target=loop.run_forever, daemon=True)
    t.start()
    #loop.run_until_complete(form.connectDiscord(loop))
    form.show()
    try:
        appx.exec_()
    except Exception as e:
        print(e)
    #print('closing loop')
    #loop.close()