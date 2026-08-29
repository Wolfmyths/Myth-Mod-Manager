import logging
import os

from PySide6.QtCore import QCoreApplication as qapp, Slot, QFile
from typing_extensions import override

from src.helpers.helper_pathing import Pathing
from src.helpers.options_manager import OptionsManager
from src.helpers.save_manager import Save
from src.objects.worker import Worker

from src.constant_vars import ModType

class DeleteMod(Worker):
    def __init__(self, *mods: str) -> None:
        super().__init__()

        self.mods: tuple[str, ...] = mods

    @override
    @Slot()
    def start(self) -> None:
        '''Removes the mod(s) from the user's computer'''

        logging.info('Deleting mods from computer: %s', ', '.join(self.mods))

        self.setTotalProgress.emit(len(self.mods))

        disPath: str = OptionsManager.getDispath()

        try: 
            for modName in self.mods:

                self.setCurrentProgress.emit(1, qapp.translate('DeleteMod', 'Deleting') + f'{modName}')

                is_enabled: bool = Save.getEnabled(modName)

                type: ModType | None = Save.getType(modName)

                if type is None:
                    logging.warning("mod %s type is none in DeleteMod.start, skipping...", modName)
                    continue

                Save.removeMods(modName)

                path: str = Pathing.mod(type, modName) if is_enabled else os.path.join(disPath, modName)

                if os.path.isdir(path):
                    QFile.moveToTrash(path)
                else:
                    logging.error('An error was raised in FileMover.deleteMod(), %s path does not exist:\n%s', os.path.basename(path), path)

                self.cancelCheck()
                self.rest()

            self.succeeded.emit()

        except Exception as e:
            self.error.emit(qapp.translate('DeleteMod', 'An error was raised while deleting a mod:') + f'\n{e}')
