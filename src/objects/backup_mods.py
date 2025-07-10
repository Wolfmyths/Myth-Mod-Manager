import os
import shutil
import logging

from PySide6.QtCore import QCoreApplication as qapp, Slot

from src.objects.worker import Worker
from src.helpers.options_manager import OptionsManager
from src.helpers.save_manager import Save
from src.helpers.helper_pathing import Pathing
from src.constant_vars import ModType, BACKUP_MODS, MODSIGNORE, MOD_CONFIG

class BackupMods(Worker):

    bundledFilePath = os.path.join(os.path.abspath(os.curdir), BACKUP_MODS)

    @Slot()
    def start(self) -> None:
            '''Takes all of the mods and compresses them into a zip file, the output is in the exe directory'''

            # Step 1: Gather Options

            disPath: str = OptionsManager.getDispath()

            # Step 2: Set Paths

            modPath: str = Pathing.mods()

            mod_overridePath: str = Pathing.mod_overrides()

            maps_path: str = Pathing.maps()

            bundledModsPath: str = os.path.join(self.bundledFilePath, 'mods')

            bundledOverridePath: str = os.path.join(self.bundledFilePath, 'assets', 'mod_overrides')

            bundledMapsPath: str = os.path.join(self.bundledFilePath, 'Maps')

            outputPathDict: dict[ModType, str] = {ModType.mods_override : bundledOverridePath, ModType.mods : bundledModsPath, ModType.maps : bundledMapsPath}

            srcPathDict: dict[ModType, str] = {ModType.mods_override : mod_overridePath, ModType.mods : modPath, ModType.maps : maps_path}

            try:

                # Step 4: Create Folders

                # Every mod
                mods = list([x for x in os.listdir(modPath) if x not in MODSIGNORE] + os.listdir(mod_overridePath) + os.listdir(disPath) + os.listdir(maps_path))

                self.setTotalProgress.emit(len(mods) + 3)

                self.setCurrentProgress.emit(1, qapp.translate('BackupMods', 'Validating backup folder paths'))

                # Creating backup environment
                for path in (self.bundledFilePath, bundledModsPath, bundledMapsPath):

                    if not os.path.isdir(path):

                        os.mkdir(path)

                # Because this dir is a nested one, needs os.makedirs unlike the others
                if not os.path.isdir(bundledOverridePath):

                    os.makedirs(bundledOverridePath)

                # Step 5: Copy each mod into the backup folder
                for mod in (x for x in mods):

                    self.setCurrentProgress.emit(1,
                        qapp.translate('BackupMods', 'Copying') +
                        f' {mod} ' +
                        qapp.translate('BackupMods', 'to') +
                        f' {BACKUP_MODS}'
                    )

                    modType: ModType | None = Save.getType(mod)

                    # In the case this file is not a mod
                    if modType is None:
                        logging.warning('File %s is not a mod or does not have an entry in %s. Skipping...', mod, MOD_CONFIG)
                        continue

                    # If the mod is disabled then the src will go to the disabled mods directory
                    src: str = os.path.join(srcPathDict[modType], mod) if Save.getEnabled(mod) else os.path.join(disPath, mod)

                    output: str = os.path.join(outputPathDict[modType], mod)

                    # shutil.copytree() can't overwrite files, so if it already exists it must be deleted first
                    if os.path.exists(output):

                        logging.info('%s already exists within the backup, overwriting...', mod)

                        shutil.rmtree(output)

                    shutil.copytree(src, output)
                    self.cancelCheck()
                    self.rest()
                
                self.cancelCheck()

                # Step 6: Zip Backup folder
                self.setCurrentProgress.emit(1,
                    qapp.translate('BackupMods', 'Zipping to') +
                    f' {self.bundledFilePath}\n' +
                    qapp.translate('BackupMods', 'This might take some time...')
                )

                # This should overwrite if it already exists
                shutil.make_archive(BACKUP_MODS, 'zip', self.bundledFilePath)

                # Step 7: Cleanup

                self.setCurrentProgress.emit(1, qapp.translate('BackupMods', 'Cleanup'))

                # Delete Folder
                shutil.rmtree(self.bundledFilePath)

                self.succeeded.emit()

            except Exception as e:
                self.onCancel()

                self.error.emit(
                    qapp.translate('BackupMods', 'An error was raised while backing up mods') +
                    f':\n{e}'
                )

    def onCancel(self) -> None:
        if os.path.exists(self.bundledFilePath):
            shutil.rmtree(self.bundledFilePath)