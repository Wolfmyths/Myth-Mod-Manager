import logging
import os

import errorChecking
from constant_vars import OPTIONS_DISPATH, MODS_DISABLED_PATH_DEFAULT

from threaded.file_mover import FileMover

class MoveToEnabledModDir(FileMover):
    def __init__(self, *mods: str):
        super().__init__()

        self.mods = mods
    
    def run(self) -> None:
        self.moveToEnableModDir(*self.mods)
        return super().run()
    
    def moveToEnableModDir(self, *mods: str) -> None:
        '''Returns a mod to their respective directory'''

        self.setTotalProgress.emit(len(mods))

        disabledModsPath = self.optionsManager.getOption(OPTIONS_DISPATH, fallback=MODS_DISABLED_PATH_DEFAULT)

        errorChecking.createDisabledModFolder()

        for mod in mods:

            if self.cancel: break

            self.setCurrentProgress.emit(1, f'Enabling {mod}')

            if mod in os.listdir(disabledModsPath):

                modDestPath = self.p.mod(self.saveManager.getType(mod), mod)

                self.move(os.path.join(disabledModsPath, mod), modDestPath)
            else:
                logging.warning('%s was not found in:\n%s\nIgnoring...', mod, disabledModsPath)
        
        self.succeeded.emit()