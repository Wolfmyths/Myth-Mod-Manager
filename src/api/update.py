import os
import shutil
import logging
import json
from typing import cast

from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PySide6.QtCore import QObject, QUrl, Signal, Slot, QDir

from src.constant_vars import IS_WINDOWS, ROOT_PATH, OLD_EXE

class Update(QObject):
    fileName: str
    exe: str

    if IS_WINDOWS:
        fileName = 'Myth-Mod-Manager.zip'
        exe = 'Myth Mod Manager.exe'
    else:
        fileName = 'Myth-Mod-Manager.tar.gz'
        exe = 'Myth Mod Manager'

    tmp = QDir.toNativeSeparators(QDir.tempPath())
    folder: str = 'Myth Mod Manager'

    doneCanceling = Signal()
    setCurrentProgress = Signal(int, str)
    addTotalProgress = Signal(int)
    setTotalProgress = Signal(int)
    downloadProgressUpdated = Signal(int, int)
    succeeded = Signal()
    error = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        logging.getLogger(__name__)

        self.network = QNetworkAccessManager(self)
        self.currentReply: QNetworkReply | None = None
        self.cancel = False
    
    def start(self) -> None:
        logging.info('Updating program...')

        LINK = 'https://api.github.com/repos/Wolfmyths/Myth-Mod-Manager/releases/latest'

        logging.info('Fetching assets_url at %s', LINK)

        self.setTotalProgress.emit(6)

        request = QNetworkRequest(QUrl(LINK))
        
        self.setCurrentProgress.emit(1, 'Getting asset_URL')

        self._cancelCheck()

        reply: QNetworkReply = self.network.get(request)
        self.currentReply = reply

        reply.finished.connect(self._handle_assetURL_fetch)
        reply.errorOccurred.connect(self._onErrorOccured)
        reply.finished.connect(reply.deleteLater)

    @Slot(int, int)
    def _on_download_progress(self, recievedBytes: int, totalBytes: int) -> None:
        self.downloadProgressUpdated.emit(recievedBytes, totalBytes)

    @Slot(QNetworkReply)
    def _handle_assetURL_fetch(self, reply: QNetworkReply) -> None:

        if not self._replyErrorCheck(reply):
            return

        self._cancelCheck()

        logging.info('Checking assets')

        data: dict[str, str] = json.loads(cast(bytearray, reply.readAll().data()).decode())

        assetUrl: str = data['assets_url']

        logging.info('Fetching asset data at %s', assetUrl)

        self.setCurrentProgress.emit(1, 'Getting asset data')

        self._cancelCheck()

        assetReply: QNetworkReply = self.network.get(QNetworkRequest(QUrl(assetUrl)))
        self.currentReply = assetReply
        assetReply.errorOccurred.connect(self._onErrorOccured)
        assetReply.finished.connect(self._download_assets)
        assetReply.finished.connect(assetReply.deleteLater)
    
    @Slot(QNetworkReply)
    def _download_assets(self, reply: QNetworkReply) -> None:

        if not self._replyErrorCheck(reply):
            return

        self._cancelCheck()

        logging.info('Fetching asset data complete')

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
        self.currentReply = downloadUpdateReply
        downloadUpdateReply.downloadProgress.connect(self._on_download_progress)
        downloadUpdateReply.errorOccurred.connect(self._onErrorOccured)
        downloadUpdateReply.finished.connect(self._install_update)
        downloadUpdateReply.finished.connect(downloadUpdateReply.deleteLater)
        
    @Slot(QNetworkReply)
    def _install_update(self, reply: QNetworkReply) -> None:

        self.currentReply = None

        if not self._replyErrorCheck(reply):
            return

        self._cancelCheck()

        downloadDir: str = os.path.join(self.tmp, self.fileName)

        logging.info('Download complete!\nWriting update to computer to %s', downloadDir)

        self.addTotalProgress.emit(3)
        self.setCurrentProgress.emit(1, 'Writing...')

        with open(downloadDir, 'wb') as f:
            f.write(reply.readAll().data())
        
        logging.info('Unzipping')

        self.setCurrentProgress.emit(1, 'Unzipping...')

        self._cancelCheck()
        
        shutil.unpack_archive(downloadDir, self.tmp)

        exe_path = os.path.join(ROOT_PATH, self.exe)

        if os.path.exists(exe_path):

            logging.info('Renaming old exe')

            self._cancelCheck()

            self.addTotalProgress.emit(1)

            self.setCurrentProgress.emit(1, 'Renaming old version...')

            os.rename(
                exe_path, 
                os.path.join(ROOT_PATH, OLD_EXE))

        self.setCurrentProgress.emit(1, 'Moving new version...')

        self._cancelCheck()

        logging.info('Moving new update to %s', ROOT_PATH)

        shutil.move(os.path.join(self.tmp, self.folder, self.exe), ROOT_PATH)

        logging.info('Update complete!')

        self.succeeded.emit()

        self.deleteLater()
    
    @Slot()
    def abort(self) -> None:
        self.cancel = True

        if self.currentReply is not None:
            self.currentReply.abort()

    @Slot()
    def _cancelCheck(self) -> None:
        if not self.cancel:
            return

        self.doneCanceling.emit()
        self.deleteLater()
    
    
    def _replyErrorCheck(self, reply: QNetworkReply) -> bool:
        ''' Returns `False` if `reply` has an error '''

        return reply.error() == QNetworkReply.NetworkError.NoError

    @Slot(QNetworkReply.NetworkError)
    def _onErrorOccured(self, err_code: QNetworkReply.NetworkError) -> None:

        if err_code == QNetworkReply.NetworkError.OperationCanceledError:
            self._cancelCheck()
            return
        
        logging.error('An error occured updating Myth Mod Manager')
        self.error.emit(err_code)
        self.deleteLater()
