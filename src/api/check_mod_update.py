import logging

from typing import cast

from PySide6.QtCore import QObject, QUrl, Signal, Slot, QVersionNumber
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply


class CheckModUpdate(QObject):
    '''
    Instancing this object will run a series of 
    functions to get the latest Myth Mod Manager version.
    '''

    updateDetected = Signal(str)
    upToDate = Signal()
    error = Signal()
    done = Signal()

    def __init__(self, modId: str, localVer: str, parent: QObject | None = None) -> None:
        super().__init__(parent=parent)
        logging.getLogger(__file__)

        try:
            self.localVer = QVersionNumber.fromString(localVer)
        except Exception as e:
            logging.error('checkModUpdate.__init__(), An error occured trying to parse mod local version %s:\n%s', localVer, str(e))
            self.error.emit()
            self.done.emit()

        link: str = f'https://api.modworkshop.net/mods/{modId}/version'

        network = QNetworkAccessManager(self)
        request = QNetworkRequest(QUrl(link))
        logging.debug('Request for %s from checkModUpdate() started', link)

        self.reply: QNetworkReply = network.get(request)
        self.reply.finished.connect(self.__reply_handler)
    
    @Slot()
    def __reply_handler(self) -> None:
        reply: QNetworkReply = cast(QNetworkReply, self.sender())

        if reply.error() == QNetworkReply.NetworkError.NoError:
            self.__checkVersion()
        else:
            logging.error('Internet error in checkModUpdate():\n%s', reply.error())
            self.error.emit()
            self.done.emit()
    
    def __checkVersion(self) -> None:
        reply: QNetworkReply = cast(QNetworkReply, self.sender())
        latestVersion = QVersionNumber()

        try:
            replyDecoded: str = cast(bytearray, reply.readAll().data()).decode()
            latestVersion= QVersionNumber.fromString(replyDecoded)
        except Exception as e:
            logging.error('An error occured trying to access a modworkshop.net API reply in checkModUpdate().__checkversion():\n%s', str(e))
            self.error.emit()
            self.done.emit()
            return

        logging.info('Latest Version: %s', latestVersion.toString())

        if latestVersion > self.localVer:
            self.updateDetected.emit(replyDecoded)
        else:
            self.upToDate.emit()
            self.done.emit()
