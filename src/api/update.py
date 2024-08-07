import os
import shutil
import logging
import json
import sys

from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PySide6.QtCore import QObject, QUrl, Signal, Slot

from src.constant_vars import ROOT_PATH, OLD_EXE

class Update(QObject):

    if sys.platform.startswith('win'):
        fileName = 'Myth-Mod-Manager.zip'
        exe = 'Myth Mod Manager.exe'
        tmp = os.environ['TEMP']
    else:
        fileName = 'Myth-Mod-Manager.tar.gz'
        exe = 'Myth Mod Manager'
        tmp = '/tmp'
    folder = 'Myth Mod Manager'

    doneCanceling = Signal()
    setCurrentProgress = Signal(int, str)
    addTotalProgress = Signal(int)
    setTotalProgress = Signal(int)
    succeeded = Signal()
    downloading = Signal(int, int)
    error = Signal(str)

    cancel = False

    def __init__(self) -> None:
        super().__init__()

        logging.getLogger(__name__)
    
    def start(self) -> None:
        logging.info('Updating program...')

        link = 'https://api.github.com/repos/Wolfmyths/Myth-Mod-Manager/releases/latest'

        logging.info('Fetching assets_url at %s', link)

        self.setTotalProgress.emit(6)

        self.network = QNetworkAccessManager()
        request = QNetworkRequest(QUrl(link))
        
        self.setCurrentProgress.emit(1, 'Getting asset_URL')

        self.__cancelCheck()

        reply = self.network.get(request)

        reply.finished.connect(self.__handle_assetURL_fetch)

    @Slot()
    def __handle_assetURL_fetch(self) -> None:

        self.__replyErrorCheck()

        logging.info('Checking assets')

        reply: QNetworkReply = self.sender()

        data: dict = json.loads(reply.readAll().data().decode())

        assetUrl: str = data['assets_url']

        logging.info('Fetching asset data at %s', assetUrl)

        self.setCurrentProgress.emit(1, 'Getting asset data')

        self.__cancelCheck()

        assetReply = self.network.get(QNetworkRequest(QUrl(assetUrl)))
        assetReply.finished.connect(self.__download_assets)
    
    @Slot()
    def __download_assets(self) -> None:

        self.__replyErrorCheck()

        self.__cancelCheck()

        logging.info('Fetching asset data complete')

        reply: QNetworkReply = self.sender()

        data: dict = json.loads(reply.readAll().data().decode())

        # Incase there are muiltiple assets create a for loop
        downloadLink: str = None

        for asset in data:
        
            if asset['name'] == self.fileName:
                
                # Found the download link
                downloadLink = asset['browser_download_url']

                break
        
        if downloadLink is not None:

            logging.info('Downloading update at %s', downloadLink)

            self.setCurrentProgress.emit(0, 'Downloading update')

            updateReply = self.network.get(QNetworkRequest(QUrl(downloadLink)))
            updateReply.downloadProgress.connect(lambda x, y: self.downloading.emit(x, y))
            updateReply.finished.connect(self.__install_update)
    
    @Slot()
    def __install_update(self) -> None:

        self.__replyErrorCheck()

        self.__cancelCheck()

        reply: QNetworkReply = self.sender()

        downloadDir = os.path.join(self.tmp, self.fileName)

        logging.info('Download complete!\nWriting update to computer to %s', downloadDir)

        self.setCurrentProgress.emit(1, 'Writing...')

        with open(downloadDir, 'wb') as f:
            f.write(reply.readAll().data())
        
        logging.info('Unzipping')

        self.setCurrentProgress.emit(1, 'Unzipping...')

        self.__cancelCheck()
        
        shutil.unpack_archive(downloadDir, self.tmp)

        if os.path.exists(os.path.join(ROOT_PATH, self.exe)):

            logging.info('Renaming old exe')

            self.__cancelCheck()

            self.addTotalProgress.emit(1)

            self.setCurrentProgress.emit(1, 'Renaming old version...')

            os.replace(self.exe, OLD_EXE)

        self.setCurrentProgress.emit(1, 'Moving new version...')

        self.__cancelCheck()

        logging.info('Moving new update to %s', ROOT_PATH)

        shutil.move(os.path.join(self.tmp, self.folder, self.exe), ROOT_PATH)

        logging.info('Update complete!')

        self.succeeded.emit()

        self.deleteLater()
    
    @Slot()
    def __cancelCheck(self) -> None:

        if self.cancel:

            self.doneCanceling.emit()
            self.deleteLater()
    
    @Slot()
    def __replyErrorCheck(self) -> None:
        reply: QNetworkReply = self.sender()

        if reply.error() != QNetworkReply.NetworkError.NoError:
            logging.error('An error occured updating Myth Mod Manager:\n%s', str(reply.error()))
            self.error.emit(str(reply.error()))
            self.deleteLater()
