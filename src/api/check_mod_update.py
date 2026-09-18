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

        self.localVer = localVer
        self.localVerVersionNumber = QVersionNumber()

        self.link: str = f'https://api.modworkshop.net/mods/{modId}/version'

        self.network = QNetworkAccessManager(self)
    
    def start(self) -> None:
        try:
            self.localVerVersionNumber = QVersionNumber.fromString(self.localVer)
        except Exception as e:
            logging.error('checkModUpdate.start(), An error occured trying to parse mod local version %s:\n%s', self.localVer, str(e))
            self.error.emit()
            self.done.emit()
            return

        request = QNetworkRequest(QUrl(self.link))
        logging.debug('Request for %s from checkModUpdate() started', self.link)

        reply: QNetworkReply = self.network.get(request)
        reply.finished.connect(self._checkVersion)
        reply.finished.connect(reply.deleteLater)
        reply.errorOccurred.connect(self._onErrorOccurred)

    @Slot(QNetworkReply.NetworkError)
    def _onErrorOccurred(self, error_code: QNetworkReply.NetworkError) -> None:

        logging.error(
            'Internet error in checkModUpdate():\n%s', error_code)

        self.error.emit()
        self.done.emit()
    
    @Slot(QNetworkReply)
    def _checkVersion(self, reply: QNetworkReply) -> None:
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

        print("Latest version:", latestVersion.toString(), "vs local Version:", self.localVerVersionNumber.toString())
        if latestVersion > self.localVerVersionNumber:
            self.updateDetected.emit(replyDecoded)
        else:
            self.upToDate.emit()
            self.done.emit()
