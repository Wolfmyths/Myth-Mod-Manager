import os
import logging

import patoolib

from src.threaded.file_mover import FileMover
from src.constant_vars import ModType

class UnZipMod(FileMover):
    def __init__(self, *mods: tuple[str, ModType]):
        super().__init__()

        self.mods = mods
    
    def run(self) -> None:
        self.unZipMod(*self.mods)
        return super().run()

    def unZipMod(self, *mods: tuple[str, ModType]) -> None:
        '''Extracts a mod and puts it into a destination based off the ModType Enum given'''

        self.setTotalProgress.emit(len(mods))

        modDestDict = {ModType.mods : self.p.mods(), ModType.mods_override : self.p.mod_overrides(), ModType.maps : self.p.maps()}

        try:

            for modURL in mods:

                src = modURL[0]

                mod = os.path.basename(src)

                modType = modURL[1]

                self.cancelCheck()

                self.setCurrentProgress.emit(1, f"Unpacking {mod}")

                logging.info('Unzipping %s to %s', src, modDestDict[modType])

                if os.path.isfile(src):
                    patoolib.extract_archive(src, outdir=modDestDict[modType])

                else:
                    logging.warning('%s does not exist', src)

            self.succeeded.emit()
        
        except patoolib.util.PatoolError as e:

            logging.error('An error was raised in FileMover.unZipMod():\n%s\nTry extracting the mod manually first', str(e))
            self.error.emit(f'An error was raised in FileMover.unZipMod():\n{e}\nTry extracting the mod manually first')

            self.cancel = True

        except Exception as e:

            logging.error('An error was raised in FileMover.unZipMod():\n%s', str(e))
            self.error.emit(f'An error was raised in FileMover.unZipMod():\n{e}')

            self.cancel = True
