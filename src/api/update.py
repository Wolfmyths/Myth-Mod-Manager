import os
import shutil
import logging
import json
import platform
from typing import cast

from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PySide6.QtCore import QObject, QUrl, Signal, Slot

from src.constant_vars import ROOT_PATH, OLD_EXE

class Update(QObject):
    fileName: str
    exe: str
    tmp: str

    if platform.system().startswith('Win'):
        fileName = 'Myth-Mod-Manager.zip'
        exe = 'Myth Mod Manager.exe'
        tmp = os.environ['TEMP']
    else:
        fileName = 'Myth-Mod-Manager.tar.gz'
        exe = 'Myth Mod Manager'
        tmp = '/tmp'
    folder: str = 'Myth Mod Manager'

    doneCanceling = Signal()
    setCurrentProgress = Signal(int, str)
    addTotalProgress = Signal(int)
    setTotalProgress = Signal(int)
    downloadProgressUpdated = Signal(int, int)
    succeeded = Signal()
    error = Signal(str)

    cancel = False

    def __init__(self) -> None:
        super().__init__()
        logging.getLogger(__name__)

        self.network = QNetworkAccessManager()
    
    def start(self) -> None:
        logging.info('Updating program...')

        LINK = 'https://api.github.com/repos/Wolfmyths/Myth-Mod-Manager/releases/latest'

        logging.info('Fetching assets_url at %s', LINK)

        self.setTotalProgress.emit(6)

        self.network = QNetworkAccessManager()
        request = QNetworkRequest(QUrl(LINK))
        
        self.setCurrentProgress.emit(1, 'Getting asset_URL')

        self.__cancelCheck()

        reply: QNetworkReply = self.network.get(request)

        reply.finished.connect(self.__handle_assetURL_fetch)

    @Slot(int, int)
    def __on_download_progress(self, recievedBytes: int, totalBytes: int) -> None:
        self.downloadProgressUpdated.emit(recievedBytes, totalBytes)

    @Slot()
    def __handle_assetURL_fetch(self) -> None:

        if not self.__replyErrorCheck():
            return

        self.__cancelCheck()

        logging.info('Checking assets')

        reply: QNetworkReply = cast(QNetworkReply, self.sender())

        data: dict[str, str] = json.loads(cast(bytearray, reply.readAll().data()).decode())

        assetUrl: str = data['assets_url']

        logging.info('Fetching asset data at %s', assetUrl)

        self.setCurrentProgress.emit(1, 'Getting asset data')

        self.__cancelCheck()

        assetReply: QNetworkReply = self.network.get(QNetworkRequest(QUrl(assetUrl)))
        assetReply.finished.connect(self.__download_assets)
    
    @Slot()
    def __download_assets(self) -> None:

        if not self.__replyErrorCheck():
            return

        self.__cancelCheck()

        logging.info('Fetching asset data complete')

        reply: QNetworkReply = cast(QNetworkReply, self.sender())

        data: list[dict[str, str]] = json.loads(cast(bytearray, reply.readAll().data()).decode())

        # Incase there are muiltiple assets create a for loop
        downloadLink: str = ''

        for asset in data:
        
            if asset['name'] == self.fileName:
                
                # Found the download link
                downloadLink = asset['browser_download_url']

                break
        
        if not downloadLink:
            self.error.emit('The key "browser_download_url" was not found in Github asset data')
            return

        logging.info('Downloading update at %s', downloadLink)

        self.setCurrentProgress.emit(0, 'Downloading update')

        downloadUpdateReply: QNetworkReply = self.network.get(QNetworkRequest(QUrl(downloadLink)))
        downloadUpdateReply.downloadProgress.connect(self.__on_download_progress)
        downloadUpdateReply.finished.connect(self.__install_update)
        
    @Slot()
    def __install_update(self) -> None:

        if not self.__replyErrorCheck():
            return

        self.__cancelCheck()

        reply: QNetworkReply = cast(QNetworkReply, self.sender())

        downloadDir: str = os.path.join(self.tmp, self.fileName)

        logging.info('Download complete!\nWriting update to computer to %s', downloadDir)

        self.addTotalProgress.emit(3)
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
    def abort(self) -> None:
        self.cancel = True

        reply = self.network.sender()

        if isinstance(reply, QNetworkReply):
            reply.abort()

    @Slot()
    def __cancelCheck(self) -> None:
        if not self.cancel:
            return

        self.doneCanceling.emit()
        self.deleteLater()
    
    
    @Slot()
    def __replyErrorCheck(self) -> bool:
        '''
        Returns a bool based on if theres an error
        '''
        reply: QNetworkReply = cast(QNetworkReply, self.sender())
        error: QNetworkReply.NetworkError = reply.error()

        if error == QNetworkReply.NetworkError.OperationCanceledError:
            self.__cancelCheck()
            return False
        
        if error != QNetworkReply.NetworkError.NoError:
            logging.error('An error occured updating Myth Mod Manager')
            self.error.emit(str(reply.error()))
            self.deleteLater()
            return False
        
        return True
