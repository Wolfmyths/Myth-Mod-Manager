import logging
import os

from PySide6.QtCore import QCoreApplication as qapp, Slot

import send2trash

from src.getPath import Pathing
from src.save import OptionsManager, Save
from src.threaded.workerQObject import Worker

from src.constant_vars import ModType

class DeleteMod(Worker):
    def __init__(self, *mods: str) -> None:
        super().__init__()

        self.mods: tuple[str, ...] = mods

    @Slot()
    def start(self) -> None:
        '''Removes the mod(s) from the user's computer'''

        logging.info('Deleting mods from computer: %s', ', '.join(self.mods))

        self.setTotalProgress.emit(len(self.mods))

        disPath: str = OptionsManager.getDispath()

        try: 
            for modName in self.mods:

                self.setCurrentProgress.emit(1, qapp.translate('DeleteMod', 'Deleting') + f'{modName}')

                enabled: bool = Save.getEnabled(modName)

                type: ModType | str | None = Save.getType(modName) if enabled else 'disabled'

                Save.removeMods(modName)

                path: list[str] | str = Pathing.mod(type, modName) if type != 'disabled' else disPath

                if os.path.isdir(path):
                    send2trash.send2trash(path)
                else:
                    logging.error('An error was raised in FileMover.deleteMod(), %s path does not exist:\n%s', os.path.basename(path), path)

                self.cancelCheck()
                self.rest()

            self.succeeded.emit()

        except Exception as e:
            self.error.emit(qapp.translate('DeleteMod', 'An error was raised while deleting a mod:') + f'\n{e}')
