import os
import logging

from src.threaded.file_mover import FileMover


class MoveToDisabledDir(FileMover):
    def __init__(self, *mods: str) -> None:
        super().__init__()

        self.mods = mods
    
    def run(self) -> None:
        self.moveToDisabledDir(*self.mods)
        return super().run()
    
    def moveToDisabledDir(self, *mods: str) -> None:
        '''Moves a mod to the disabled folder'''

        self.setTotalProgress.emit(len(mods))

        disabledModsPath = self.optionsManager.getDispath()

        try:

            for mod in mods:

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
            logging.error('An error occured while disabling a mod:\n%s', str(e))
            self.error.emit(f'An error occured while disabling a mod:\n{e}')

            self.cancel = True
