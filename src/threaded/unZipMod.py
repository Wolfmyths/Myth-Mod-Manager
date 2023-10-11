import os
import logging

import patoolib

from PySide6.QtCore import QUrl

from threaded.file_mover import FileMover
from constant_vars import ModType

class UnZipMod(FileMover):
    def __init__(self, *mods: tuple[QUrl, str]):
        super().__init__()

        self.mods = mods
    
    def run(self) -> None:
        self.unZipMod(*self.mods)
        return super().run()

    def unZipMod(self, *mods: tuple[QUrl, str]) -> None:
        '''Extracts a mod and puts it into a destination based off the type given'''

        self.setTotalProgress.emit(len(mods))

        modDestDict = {ModType.maps : self.p.mods(), ModType.maps : self.p.mod_overrides(), ModType.maps : self.p.maps()}

        try:

            for modURL in mods:

                url = modURL[0]

                src = url.toLocalFile()

                mod = url.fileName()

                type = modURL[1]

                if self.cancel: break

                self.setCurrentProgress.emit(1, f"Unpacking {mod}")

                if os.path.exists(src):

                    patoolib.extract_archive(src, outdir=modDestDict[type])

        except Exception as e:

            logging.error('An error was raised in FileMover.unZipMod():\n%s', str(e))

            self.error.emit(str(e))
        
        self.succeeded.emit()
