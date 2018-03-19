import logging
import sys

from PyQt5 import QtWidgets

from app import app
from app.signaler import QtSignaler
from app.apiClients import discordClient

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    signaler = QtSignaler()
    appx = QtWidgets.QApplication(sys.argv)
    form = app.FusionChat(signaler=signaler)
    
    #loop.run_until_complete(form.connectDiscord(loop))
    form.show()
    try:
        appx.exec_()
    except Exception as e:
        logging.error(e)
    #print('closing loop')
    #loop.close()