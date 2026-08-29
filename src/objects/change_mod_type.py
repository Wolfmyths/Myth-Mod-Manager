import logging
import os

from PySide6.QtCore import QCoreApplication as qapp, Slot
from typing_extensions import override

from src.helpers.helper_pathing import Pathing
import src.helpers.helper as helper
from src.objects.worker import Worker
from src.constant_vars import ModType

class ChangeModType(Worker):
    def __init__(self, *mods: tuple[str, ModType]) -> None:
        super().__init__()
        logging.getLogger(__name__)

        self.mods: tuple[tuple[str, ModType], ...] = mods
        self.mods_moved: list[tuple[str, str]] = []
    
    @override
    @Slot()
    def start(self) -> None:
        '''
        Moves the mod to a new directory
        '''

        self.setTotalProgress.emit(len(self.mods))
        
        for mod_tuple in self.mods:

            modsDirPath: str = mod_tuple[0]
            ChosenDir: ModType = mod_tuple[1]

            mod: str = os.path.basename(modsDirPath)

            self.setCurrentProgress.emit(1, qapp.translate('ChangeModType', 'Installing') + f' {mod}')

            # Setting the Destination path
            if helper.isTypeMod(ChosenDir):

                modDestPath: str = Pathing.mod(ChosenDir, mod)

                self.move(modsDirPath, modDestPath)
                self.mods_moved.append((modsDirPath, modDestPath))

            self.cancelCheck()
            self.rest()

        
        self.succeeded.emit()
    
    @override
    def onCancel(self) -> None:
        self.setTotalProgress.emit(len(self.mods_moved))
        for modPaths in self.mods_moved:
            self.setCurrentProgress.emit(1, qapp.translate('ChangeModType', 'Uninstalling') + f' {os.path.basename(modPaths[0])}')
            self.move(modPaths[1], modPaths[0])
            self.rest()

