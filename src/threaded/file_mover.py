import shutil
import os
import logging

from save import Save, OptionsManager
from getPath import Pathing
import errorChecking
from threaded.QThread import Thread


class FileMover(Thread):
    '''
    Base class for threaded functions involving file manipulation
    '''

    def __init__(self):
        super().__init__()

        logging.getLogger(__name__)

        self.saveManager = Save()
        self.optionsManager = OptionsManager()

        self.p = Pathing()

    def onError(self, func, path, exc_info):
        """Used for `shutil.rmtree()`s `onerror` kwarg"""

        logging.warning('An error was raised in shutil:\n%s', exc_info)

        if not errorChecking.permissionCheck(path):

            func(path)
    
    def move(self, src: str, dest: str):
        '''`shutil.move()` with some extra exception handling'''

        # Overwrite mod
        if os.path.exists(dest):
            shutil.rmtree(dest, onerror=self.onError)

        # Will try to move the file, if there is an exception, fix the issue and try again
        while True and not self.cancel:

            try:
                shutil.move(src, dest)
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

                self.setCurrentProgress.emit(1, f'Fixing install for {src.split("/")[-1]}')
                # If shutil.move made a partial dir of the mod delete it
                if os.path.exists(dest):
                    shutil.rmtree(dest, onerror=self.onError)
