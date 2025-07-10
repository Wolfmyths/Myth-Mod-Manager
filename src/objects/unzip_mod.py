import os
import logging

import patoolib

from PySide6.QtCore import QCoreApplication as qapp, Slot

from src.helpers.helper_pathing import Pathing
from src.objects.worker import Worker
from src.constant_vars import ModType

class UnZipMod(Worker):
    def __init__(self, *mods: tuple[str, ModType]) -> None:
        super().__init__()

        self.mods: tuple[tuple[str, ModType], ...] = mods

    @Slot()
    def start(self) -> None:
        '''Extracts a mod and puts it into a destination based off the ModType Enum given'''

        self.setTotalProgress.emit(len(self.mods))

        modDestDict: dict[ModType, str] = {
            ModType.mods          : Pathing.mods(),
            ModType.mods_override : Pathing.mod_overrides(),
            ModType.maps          : Pathing.maps()
        }

        try:

            for modURL in self.mods:

                src: str = modURL[0]

                mod: str = os.path.basename(src)

                modType: ModType = modURL[1]

                self.setCurrentProgress.emit(1, qapp.translate("UnZipMod", "Unpacking") + f" {mod}")

                logging.info('Unzipping %s to %s', src, modDestDict[modType])

                if os.path.isfile(src):
                    patoolib.extract_archive(src, outdir=modDestDict[modType])

                else:
                    logging.warning('%s does not exist', src)

                self.cancelCheck()
                self.rest()

            self.succeeded.emit()
        
        except patoolib.util.PatoolError as e:
            self.error.emit(
                qapp.translate("UnZipMod", 'An error was raised in unZipMod:') +
                f'\n{e}\n' +
                qapp.translate("UnZipMod", 'Try extracting the mod manually first')
            )

        except Exception as e:
            self.error.emit(
                qapp.translate("UnZipMod", 'An error was raised in unZipMod:') + f'\n{e}') 
