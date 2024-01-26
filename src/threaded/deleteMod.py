import logging
import os
import shutil

from src.threaded.workerQObject import Worker

from src.constant_vars import MOD_CONFIG, OPTIONS_CONFIG

class DeleteMod(Worker):
    def __init__(self, *mods: str, optionsPath: str = OPTIONS_CONFIG, savePath: str = MOD_CONFIG):
        super().__init__(optionsPath=optionsPath, savePath=savePath)

        self.mods = mods

    def start(self) -> None:
        '''Removes the mod(s) from the user's computer'''

        logging.info('Deleting mods from computer: %s', ', '.join(self.mods))

        self.setTotalProgress.emit(len(self.mods))

        disPath = self.optionsManager.getDispath()

        try: 
            for modName in self.mods:

                self.cancelCheck()

                self.setCurrentProgress.emit(1, f'Deleting {modName}')

                enabled = self.saveManager.getEnabled(modName)

                type = self.saveManager.getType(modName) if enabled else 'disabled'

                self.saveManager.removeMods(modName)

                path = self.p.mod(type, modName) if type != 'disabled' else disPath

                if os.path.isdir(path):
                    shutil.rmtree(path, onerror=self.onError)
                else:
                    logging.error('An error was raised in FileMover.deleteMod(), %s path does not exist:\n%s', os.path.basename(path), path)

            self.succeeded.emit()

        except Exception as e:
            self.error.emit(f'An error has occured in deleteMod():\n{e}')
