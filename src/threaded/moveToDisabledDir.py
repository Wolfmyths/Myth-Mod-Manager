import os
import logging

from PySide6.QtCore import QCoreApplication as qapp, Slot

from src.threaded.workerQObject import Worker

from src.constant_vars import MOD_CONFIG, OPTIONS_CONFIG

class MoveToDisabledDir(Worker):
    def __init__(self, *mods: str, optionsPath: str = OPTIONS_CONFIG, savePath: str = MOD_CONFIG) -> None:
        super().__init__(optionsPath=optionsPath, savePath=savePath)

        self.mods = mods

    @Slot()
    def start(self) -> None:
        '''Moves a mod to the disabled folder'''

        self.setTotalProgress.emit(len(self.mods))

        disabledModsPath = self.optionsManager.getDispath()

        try:

            for mod in self.mods:

                self.cancelCheck()

                self.setCurrentProgress.emit(1, qapp.translate('MoveToDisabledDir', 'Disabling') + f' {mod}')

                modDest = os.path.join(disabledModsPath, mod)

                # Checking if the mod is already in the disabled mods folder
                if not os.path.isdir(modDest):

                    modPath = self.p.mod(self.saveManager.getType(mod), mod)

                    self.move(modPath, modDest)
                else:
                    logging.info('%s is already in the disabled directory', mod)

            self.succeeded.emit()

        except Exception as e:
            self.error.emit(qapp.translate('MoveToDisabledDir', 'An error occured while disabling a mod:') + f'\n{e}')
