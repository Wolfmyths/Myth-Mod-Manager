import logging

from PySide6.QtCore import QUrl

import errorChecking
from threaded.file_mover import FileMover
from constant_vars import ModType

class ChangeModType(FileMover):
    def __init__(self, *mods: tuple[QUrl, ModType]):
        super().__init__()

        self.mods = mods

    def run(self) -> None:
        self.changeModType(*self.mods)
        return super().run()
    
    def changeModType(self, *mods: tuple[QUrl, ModType]) -> None:
        '''
        Moves the mod to a new directory
        '''

        try:
            self.setTotalProgress.emit(len(mods))

            ChosenDir = None
            
            for mod in mods:

                self.cancelCheck()

                modURL = mod[0]
                ChosenDir = mod[1]

                modsDirPath = modURL.toLocalFile()

                mod = modURL.fileName()

                self.setCurrentProgress.emit(1, f'Installing {mod}')

                # Setting the Destination path
                if errorChecking.isTypeMod(ChosenDir):

                    modDestPath = self.p.mod(ChosenDir, mod)

                    self.move(modsDirPath, modDestPath)
            
            self.succeeded.emit()

        except Exception as e:
            logging.error('An error occured in changeModType:\n%s', str(e))
            self.error.emit(str(e))
            self.cancel = True
