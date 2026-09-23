import os
import logging

import patoolib  # pyright: ignore[reportMissingTypeStubs]

from PySide6.QtCore import QCoreApplication as qapp, QMutex, QObject, Slot
from typing_extensions import override

from src.helpers.helper_pathing import Pathing
from src.objects.worker import Worker
from src.constant_vars import ModType

class UnZipMod(Worker):
    def __init__(self, *mods: tuple[str, ModType], parent: QObject | None = None, mutex: QMutex | None = None) -> None:
        super().__init__(parent, mutex)

        self.mods: tuple[tuple[str, ModType], ...] = mods

    @override
    def onCancel(self) -> None:
        return

    @override
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

            for src, modType in self.mods:

                mod: str = os.path.basename(src)

                self.setCurrentProgress.emit(1, qapp.translate("UnZipMod", "Unpacking") + f" {mod}")

                logging.info('Unzipping %s to %s', src, modDestDict[modType])

                if os.path.isfile(src):
                    logging.debug("Extracting Archive")
                    patoolib.extract_archive(src, outdir=modDestDict[modType])

                else:
                    logging.warning('%s does not exist or is not a file', src)

                logging.debug("Starting cancel check")
                self.cancelCheck()
                logging.debug("Resting")
                self.rest()

            self.succeeded.emit()
        
        except patoolib.util.PatoolError as e:
            logging.error(f"PatoolError: {e}")
            self.error.emit(
                qapp.translate("UnZipMod", 'An error was raised in unZipMod:') +
                f'\n{e}\n' +
                qapp.translate("UnZipMod", 'Try extracting the mod manually first')
            )

        except Exception as e:
            logging.error(f"Error: {e.__class__} {e}")
            self.error.emit(
                qapp.translate("UnZipMod", 'An error was raised in unZipMod:') + f'\n{e}') 
