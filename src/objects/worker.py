import logging
import os
import shutil
from collections.abc import Callable
from typing import Any

from PySide6.QtCore import QCoreApplication as qapp
from PySide6.QtCore import QObject, Signal, QMutex, QMutexLocker

import src.helpers.helper as helper

class Worker(QObject):
    setTotalProgress = Signal(int)

    addTotalProgress = Signal(int)

    setCurrentProgress = Signal(int, str)

    succeeded = Signal()

    doneCanceling = Signal()

    error = Signal(str)

    cancel = False

    mutex: QMutex = None # Should be set externally by the ProgressWidget class

    def __init__(self) -> None:
        super().__init__()
        logging.getLogger(__name__)

    def start() -> None:
        ...

    def onCancel(self) -> None:
        ...

    def rest(self) -> None:
        '''
        Emits signals too fast even with signal blockers so we need this until we can find a better way
        '''
        self.thread().msleep(1)

    def cancelCheck(self) -> None:
        with QMutexLocker(self.mutex):
            if not self.cancel:
                return
        
        logging.info('%s was canceled', self.__class__)
        self.onCancel()
        self.doneCanceling.emit()

    def move(self, src: str, dest: str) -> None:
        '''`shutil.move()` with some extra exception handling'''

        # Overwrite mod
        if os.path.exists(dest):
            shutil.rmtree(dest, onerror=self.onError)

        # Will try to move the file, if there is an exception, fix the issue and try again
        try:
            shutil.move(src, dest)
            logging.info('Moved file %s to destination %s', src, dest)

        except PermissionError:
            
            # Grab all files in mod
            for root, dirs, files in os.walk(src):

                self.addTotalProgress.emit(2 + len(dirs) + len(files))
                
                # Checking files for perm errors
                for file in files:
                    self.setCurrentProgress.emit(1, qapp.translate('Worker', 'Checking file permissions of') + f' {file}')
                    file_path = os.path.join(root, file)
                    helper.permissionCheck(file_path)
                
                # Checking folders for perm errors
                for dir in dirs:
                    self.setCurrentProgress.emit(1, qapp.translate('Worker', 'Checking folder permissions of') + f' {dir}')
                    dir_path = os.path.join(root, dir)
                    helper.permissionCheck(dir_path)
                
                # Checking mod directory for perm errors
                self.setCurrentProgress.emit(1, qapp.translate('Worker', 'Checking folder permissions of') + f' {root}')
                helper.permissionCheck(root)

            self.setCurrentProgress.emit(1, qapp.translate('Worker', 'Fixing install for') + f' {os.path.basename(src)}')
            # If shutil.move made a partial dir of the mod delete it
            if os.path.exists(dest):
                shutil.rmtree(dest, onerror=self.onError)

    def onError(self, func: Callable[[Any], Any], path: str, exc_info: int) -> None:
        """Used for `shutil.rmtree()`s `onerror` kwarg"""

        logging.warning('An error was raised in shutil:\n%s', exc_info)

        if not helper.permissionCheck(path):

            func(path)
