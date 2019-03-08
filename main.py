import sys

from PyQt5 import QtWidgets

from fusionchat import app
from fusionchat.signaler import QtSignaler

import logging
logger = logging.getLogger("fusionchat")

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    logger.setLevel(logging.DEBUG)
    signaler = QtSignaler()
    appx = QtWidgets.QApplication(sys.argv)
    form = app.FusionChat(signaler=signaler)
    
    #loop.run_until_complete(form.connectDiscord(loop))
    form.show()
    try:
        appx.exec_()
    except Exception as e:
        logger.error(e)
    #print('closing loop')
    #loop.close()