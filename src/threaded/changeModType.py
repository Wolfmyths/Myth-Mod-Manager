import logging
import os

import src.errorChecking as errorChecking
from src.threaded.workerQObject import Worker
from src.constant_vars import ModType

class ChangeModType(Worker):
    def __init__(self, *mods: tuple[str, ModType]):
        super().__init__()
        logging.getLogger(__name__)

        self.mods = mods
    
    def start(self) -> None:
        '''
        Moves the mod to a new directory
        '''

        try:
            self.setTotalProgress.emit(len(self.mods))

            ChosenDir = None
            
            for mod in self.mods:

                self.cancelCheck()

                modsDirPath = mod[0]
                ChosenDir = mod[1]

                mod = os.path.basename(modsDirPath)

                self.setCurrentProgress.emit(1, f'Installing {mod}')

                # Setting the Destination path
                if errorChecking.isTypeMod(ChosenDir):

                    modDestPath = self.p.mod(ChosenDir, mod)

                    self.move(modsDirPath, modDestPath)
            
            self.succeeded.emit()

        except Exception as e:
            self.error.emit(f'An error occured in changeModType:\n{e}')
