import logging
import os
import shutil

from PySide6.QtCore import Signal, QObject

from src.save import Save, OptionsManager
from src.getPath import Pathing
import src.errorChecking as errorChecking

from src.constant_vars import MOD_CONFIG, OPTIONS_CONFIG

class MoveToEnabledModDir(QObject):
    
    setTotalProgress = Signal(int)

    addTotalProgress = Signal(int)

    setCurrentProgress = Signal(int, str)

    succeeded = Signal()

    doneCanceling = Signal()

    error = Signal(str)

    cancel = False

    def __init__(self, *mods: str, optionsPath: str = OPTIONS_CONFIG, savePath: str = MOD_CONFIG):
        super().__init__()

        self.mods = mods

        logging.getLogger(__name__)

        self.saveManager = Save(savePath)
        self.optionsManager = OptionsManager(optionsPath)

        self.p = Pathing(optionsPath)

    def start(self) -> None:
        '''Returns a mod to their respective directory'''

        try:

            self.setTotalProgress.emit(len(self.mods))

            disabledModsPath = self.optionsManager.getDispath()

            for mod in self.mods:

                #self.cancelCheck()

                self.setCurrentProgress.emit(1, f'Enabling {mod}')

                if mod in os.listdir(disabledModsPath):

                    modDestPath = self.p.mod(self.saveManager.getType(mod), mod)

                    self.move(os.path.join(disabledModsPath, mod), modDestPath)
                else:
                    logging.warning('%s was not found in:\n%s\nIgnoring...', mod, disabledModsPath)
            
            self.succeeded.emit()

        except Exception as e:
            logging.error('An error occured while enabling a mod:\n%s', str(e))
            self.error.emit(f'An error occured while enabling a mod:\n{e}')

            self.cancel = True

    def move(self, src: str, dest: str):
        '''`shutil.move()` with some extra exception handling'''

        # Overwrite mod
        if os.path.exists(dest):
            shutil.rmtree(dest, onerror=self.onError)

        # Will try to move the file, if there is an exception, fix the issue and try again
        while True and not self.cancel:

            try:
                shutil.move(src, dest)
                logging.info('Moved file %s to destination %s', src, dest)
                break

            except PermissionError:
                
                # Grab all files in mod
                for root, dirs, files in os.walk(src):

                    self.addTotalProgress.emit(2 + len(dirs) + len(files))
                    
                    # Checking files for perm errors
                    for file in files:
                        self.setCurrentProgress.emit(1, f'Checking file permissions of {file}')
                        file_path = os.path.join(root, file)
                        errorChecking.permissionCheck(file_path)
                    
                    # Checking folders for perm errors
                    for dir in dirs:
                        self.setCurrentProgress.emit(1, f'Checking folder permissions of {dir}')
                        dir_path = os.path.join(root, dir)
                        errorChecking.permissionCheck(dir_path)
                    
                    # Checking mod directory for perm errors
                    self.setCurrentProgress.emit(1, f'Checking folder permissions of {root}')
                    errorChecking.permissionCheck(root)

                self.setCurrentProgress.emit(1, f'Fixing install for {os.path.basename(src)}')
                # If shutil.move made a partial dir of the mod delete it
                if os.path.exists(dest):
                    shutil.rmtree(dest, onerror=self.onError)

    def onError(self, func, path, exc_info):
        """Used for `shutil.rmtree()`s `onerror` kwarg"""

        logging.warning('An error was raised in shutil:\n%s', exc_info)

        if not errorChecking.permissionCheck(path):

            func(path)  
