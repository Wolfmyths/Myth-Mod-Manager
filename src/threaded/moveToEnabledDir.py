import logging
import os

from src.threaded.workerQObject import Worker

from src.constant_vars import MOD_CONFIG, OPTIONS_CONFIG

class MoveToEnabledModDir(Worker):

    def __init__(self, *mods: str, optionsPath: str = OPTIONS_CONFIG, savePath: str = MOD_CONFIG):
        super().__init__(optionsPath=optionsPath, savePath=savePath)

        self.mods = mods

    def start(self) -> None:
        '''Returns a mod to their respective directory'''

        try:

            self.setTotalProgress.emit(len(self.mods))

            disabledModsPath = self.optionsManager.getDispath()

            for mod in self.mods:

                self.cancelCheck()

                self.setCurrentProgress.emit(1, f'Enabling {mod}')

                modPath = os.path.join(disabledModsPath, mod)

                if os.path.isdir(modPath):

                    modDestPath = self.p.mod(self.saveManager.getType(mod), mod)

                    self.move(modPath, modDestPath)
                else:
                    logging.warning('%s was not found in:\n%s\nIgnoring...', mod, disabledModsPath)
            
            self.succeeded.emit()

        except Exception as e:
            self.error.emit(f'An error occured while enabling a mod:\n{e}')
