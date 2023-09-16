import os
import shutil
import logging

import requests

from PySide6.QtCore import QThread, Signal

from constant_vars import ROOT_PATH

class Update(QThread):

    setTotalProgress = Signal(int)

    addTotalProgress = Signal(int)

    setCurrentProgress = Signal(int, str)

    succeeded = Signal()

    doneCanceling = Signal()

    error = Signal(str)

    cancel = False

    fileName = 'Myth-Mod-Manager.zip'
    exe = 'Myth Mod Manager.exe' 
    folder = 'Myth Mod Manager'

    def run(self) -> None:

        logging.getLogger(__name__)

        logging.info('Starting thread to update program...')

        self.downloadUpdate()

        return super().run()

    def downloadUpdate(self):

        try:

            self.setTotalProgress.emit(7)
            
            self.setCurrentProgress.emit(0, 'Fetching latest version release info on github.com')

            self.cancelCheck()

            # Get latest release data
            latestRelease = requests.get('https://api.github.com/repos/Wolfmyths/Myth-Mod-Manager/releases/latest')

            # Find asset data api link
            assetUrl = latestRelease.json()['assets_url']

            self.setCurrentProgress.emit(1, 'Fetching asset data from github.com')

            self.cancelCheck()

            # Get asset data
            assetsData: dict = requests.get(assetUrl , headers={'accept':'application/vnd.github+json'}).json()

            # Incase there are muiltiple assets create a for loop
            downloadLink: str = None
            downloadSize: int = None

            for asset in assetsData:
            
                if asset['name'] == self.fileName:
                    
                    # Found the download link
                    downloadLink = asset['browser_download_url']
                    downloadSize = int(asset['size'])

                    break
            
            if downloadLink:

                # Instance a session
                session = requests.Session()

                # Creating a new file in 'write in binary' mode
                with open(self.fileName, 'wb') as f:

                    self.setCurrentProgress.emit(1, 'Fetching download for download...')

                    self.cancelCheck()

                    # Get data for download
                    request = session.get(downloadLink, allow_redirects=True, stream=True)

                    chunkSize = 1024

                    totalChunks = downloadSize // chunkSize

                    currentChunks = 0

                    self.addTotalProgress.emit(totalChunks // chunkSize)

                    self.setCurrentProgress.emit(1, 'Fetching data for download...')

                    # Write it to fileName in chunks
                    chunk: bytes
                    for chunk in request.iter_content(chunkSize**2):

                        self.cancelCheck()

                        self.setCurrentProgress.emit(1, f'Downloading Myth Mod Manager... {int(currentChunks / totalChunks * 100)}%')

                        f.write(chunk)

                        currentChunks += chunkSize
                    
                    logging.info('Finished downloading update')

            # Installation

            directory = os.listdir(ROOT_PATH)

            if self.fileName in directory:
                
                self.cancelCheck()    

                self.setCurrentProgress.emit(1, 'Unzipping the new update...')

                shutil.unpack_archive(self.fileName)

                if self.exe in directory:

                    self.cancelCheck()

                    self.addTotalProgress.emit(1)

                    self.setCurrentProgress.emit(1, 'Renaming old version...')

                    os.rename(self.exe, f'{self.exe} (Old)')

                self.setCurrentProgress.emit(1, 'Moving new version...')

                self.cancelCheck()

                shutil.move(os.path.join(self.folder, self.exe), ROOT_PATH)

                self.setCurrentProgress.emit(1, 'Clean up...')

                os.remove(self.fileName)

                os.rmdir(self.folder)

                logging.info('Done')

                self.succeeded.emit()

        except Exception as e:

            directory = os.listdir(ROOT_PATH)

            if self.folder in directory:

                shutil.rmtree(self.folder)
            
            if self.fileName in directory:

                os.remove(self.fileName)
            
            logging.error('Error at Update.downloadUpdate():\n%s', str(e))

            self.error.emit(str(e))
    
    def cancelCheck(self):

        if self.cancel:

            self.doneCanceling.emit()
