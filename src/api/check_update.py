import json
import logging
from typing import cast

from PySide6.QtCore import QObject, QUrl, Signal, Slot, QVersionNumber
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

from src.constant_vars import VERSION

class CheckUpdate(QObject):
    '''
    This object will run a series of 
    functions to get the latest Myth Mod Manager version.

    `Use CheckUpdate.start() to begin`
    '''

    updateDetected = Signal(str, str)
    upToDate = Signal()
    error = Signal()
    done = Signal()

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent=parent)
        logging.getLogger(__file__)
    
    def start(self) -> None:
        link = 'https://api.github.com/repos/Wolfmyths/Myth-Mod-Manager/releases/latest'
        
        network = QNetworkAccessManager(self)
        request = QNetworkRequest(QUrl(link))
        logging.debug('Request for %s from checkUpdate() started', link)
        
        reply: QNetworkReply = network.get(request)
        reply.finished.connect(self.__reply_handler)

    @Slot()
    def __reply_handler(self) -> None:
        reply: QNetworkReply = cast(QNetworkReply, self.sender())

        if reply.error() == QNetworkReply.NetworkError.NoError:
            self.__checkVersion()
        else:
            logging.error('Internet error in checkUpdate():\n%s', reply.error())
            self.error.emit()
            self.done.emit()
    
    def __checkVersion(self) -> None:
        reply: QNetworkReply = cast(QNetworkReply, self.sender())

        try:
            data: dict = json.loads(cast(bytearray, reply.readAll().data()).decode())  # pyright: ignore[reportMissingTypeArgument]
        except Exception as e:
            logging.error('An error occured trying to access a Github API reply in checkUpdate().__checkversion():\n%s', str(e))
            self.error.emit()
            self.done.emit()
            return

        latestVersion = QVersionNumber.fromString(data['tag_name'])  # pyright: ignore[reportUnknownArgumentType]
        
        logging.info('Latest Version: %s', latestVersion)

        if latestVersion > VERSION:
            self.updateDetected.emit(latestVersion, data['body'])
        else:
            self.upToDate.emit()
            self.done.emit()
