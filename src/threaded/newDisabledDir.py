import logging
import os

from PySide6.QtCore import QCoreApplication as qapp, Slot

from src.threaded.workerQObject import Worker

class NewDisabledDir(Worker):

    def __init__(self, old_path: str, new_path: str) -> None:
        super().__init__()

        self.old_path: str = old_path
        self.new_path: str = new_path
        self.mods_to_move: list[str] = os.listdir(self.old_path)
        self.mods_moved: list[str] = []

    @Slot()
    def start(self) -> None:
        '''Moves disabled mods to a new folder'''

        self.setTotalProgress.emit(len(self.mods_to_move))

        for mod in self.mods_to_move:

            self.setCurrentProgress.emit(1, qapp.translate('NewDisabledDir', 'Moving') + f' {mod}')

            modDestPath: str = os.path.join(self.new_path, mod)
            modCurrentPath: str = os.path.join(self.old_path, mod)

            if os.path.isdir(modCurrentPath):

                self.move(modCurrentPath, modDestPath)
                self.mods_moved.append(mod)
                self.mods_to_move.remove(mod)
            else:
                logging.warning('%s was not found in:\n%s\nIgnoring...', mod, modCurrentPath)

            self.cancelCheck()
            self.rest()
        
        self.succeeded.emit()
    
    def onCancel(self) -> None:
        self.setTotalProgress.emit(len(self.mods_moved))

        for mod in self.mods_moved:
            self.setCurrentProgress.emit(1, qapp.translate('NewDisabledDir', 'Moving') + f' {mod}')

            modDestPath: str = os.path.join(self.old_path, mod)
            modCurrentPath: str = os.path.join(self.new_path, mod)

            self.move(modCurrentPath, modDestPath)
            self.rest()
