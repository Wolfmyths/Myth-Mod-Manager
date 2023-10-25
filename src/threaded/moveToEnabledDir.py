import logging
import os

from src.threaded.file_mover import FileMover

class MoveToEnabledModDir(FileMover):
    def __init__(self, *mods: str):
        super().__init__()

        self.mods = mods
    
    def run(self) -> None:
        self.moveToEnableModDir(*self.mods)
        return super().run()
    
    def moveToEnableModDir(self, *mods: str) -> None:
        '''Returns a mod to their respective directory'''

        try:

            self.setTotalProgress.emit(len(mods))

            disabledModsPath = self.optionsManager.getDispath()

            for mod in mods:

                self.cancelCheck()

                self.setCurrentProgress.emit(1, f'Enabling {mod}')

                if mod in os.listdir(disabledModsPath):

                    modDestPath = self.p.mod(self.saveManager.getType(mod), mod)

                    self.move(os.path.join(disabledModsPath, mod), modDestPath)
                else:
                    logging.warning('%s was not found in:\n%s\nIgnoring...', mod, disabledModsPath)
            
            self.succeeded.emit()

        except Exception as e:
            logging.error('An error occured while enabling a mod:\n%s', str(e))
            self.error.emit(f'An error occured while enabling a mod:\n{e}')

            self.cancel = True            
