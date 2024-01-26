import os
import logging

from src.threaded.workerQObject import Worker

from src.constant_vars import MOD_CONFIG, OPTIONS_CONFIG

class MoveToDisabledDir(Worker):
    def __init__(self, *mods: str, optionsPath: str = OPTIONS_CONFIG, savePath: str = MOD_CONFIG) -> None:
        super().__init__(optionsPath=optionsPath, savePath=savePath)

        self.mods = mods

    def start(self) -> None:
        '''Moves a mod to the disabled folder'''

        self.setTotalProgress.emit(len(self.mods))

        disabledModsPath = self.optionsManager.getDispath()

        try:

            for mod in self.mods:

                self.cancelCheck()

                self.setCurrentProgress.emit(1, f'Disabling {mod}')

                # Checking if the mod is already in the disabled mods folder
                if not mod in os.listdir(disabledModsPath):

                    modPath = self.p.mod(self.saveManager.getType(mod), mod)

                    self.move(modPath, os.path.join(disabledModsPath, mod))
                else:
                    logging.info('%s is already in the disabled directory', mod)

            self.succeeded.emit()

        except Exception as e:
            self.error.emit(f'An error occured while disabling a mod:\n{e}')
