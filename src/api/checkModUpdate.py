import logging

from PySide6.QtCore import QObject, QUrl, Signal
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

from semantic_version import Version


class checkModUpdate(QObject):
    '''
    Instancing this object will run a series of 
    functions to get the latest Myth Mod Manager version.

    `checkUpdate` will delete itself after it's finished.
    '''

    updateDetected = Signal(str)
    upToDate = Signal()
    error = Signal()

    def __init__(self, modId: str, localVer: str) -> None:
        super().__init__()
        logging.getLogger(__file__)

        try:
            self.localVer = Version.coerce(localVer)
        except Exception as e:
            logging.error('checkModUpdate.__init__(), An error occured trying to parse mod local version %s:\n%s', localVer, str(e))
            self.error.emit()
            self.deleteLater()

        link = f'https://api.modworkshop.net/mods/{modId}/version'

        network = QNetworkAccessManager(self)
        request = QNetworkRequest(QUrl(link))
        logging.debug('Request for %s from checkModUpdate() started', link)

        self.reply = network.get(request)
        self.reply.finished.connect(self.__reply_handler)
    
    def __reply_handler(self) -> None:
        reply: QNetworkReply = self.sender()

        if reply.error() == QNetworkReply.NetworkError.NoError:
            self.__checkVersion()
        else:
            logging.error('Internet error in checkModUpdate():\n%s', reply.error())
            self.error.emit()
            self.deleteLater()
    
    def __checkVersion(self) -> None:
        reply: QNetworkReply = self.sender()

        replyDecoded = reply.readAll().data().decode()

        try:
            latestVersion = Version.coerce(replyDecoded)
        except Exception as e:
            logging.error('An error occured trying to access a modworkshop.net API reply in checkModUpdate().__checkversion():\n%s', str(e))
            self.error.emit()
            self.deleteLater()

        logging.info('Latest Version: %s', latestVersion)

        if latestVersion > self.localVer:
            self.updateDetected.emit(replyDecoded)
        else:
            self.upToDate.emit()

        self.deleteLater()
