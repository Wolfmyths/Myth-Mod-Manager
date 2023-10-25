import os
import shutil
import logging

from src.threaded.file_mover import FileMover
from src.constant_vars import ModType, BACKUP_MODS, MODSIGNORE, MOD_CONFIG

class BackupMods(FileMover):
    def run(self) -> None:
        self.backupMods()
        return super().run()

    def backupMods(self) -> None:
            '''Takes all of the mods and compresses them into a zip file, the output is in the exe directory'''

            # Step 1: Gather Options

            disPath = self.optionsManager.getDispath()

            # Step 2: Set Paths

            modPath = self.p.mods()

            mod_overridePath = self.p.mod_overrides()

            maps_path = self.p.maps()

            bundledFilePath = os.path.join(os.path.abspath(os.curdir), BACKUP_MODS)

            bundledModsPath = os.path.join(bundledFilePath, 'mods')

            bundledOverridePath = os.path.join(bundledFilePath, 'assets', 'mod_overrides')

            bundledMapsPath = os.path.join(bundledFilePath, 'Maps')

            outputPathDict = {ModType.mods_override : bundledOverridePath, ModType.mods : bundledModsPath, ModType.maps : bundledMapsPath}

            srcPathDict = {ModType.mods_override : mod_overridePath, ModType.mods : modPath, ModType.maps : maps_path}

            # Define error msg

            try:

                # Step 4: Create Folders

                # Every mod
                mods = list([x for x in os.listdir(modPath) if x not in MODSIGNORE] + os.listdir(mod_overridePath) + os.listdir(disPath) + os.listdir(maps_path))

                self.setTotalProgress.emit(len(mods) + 3)

                self.setCurrentProgress.emit(1, f'Validating backup folder paths')

                # Creating backup environment
                for path in (bundledFilePath, bundledModsPath, bundledMapsPath):

                    if not os.path.isdir(path):

                        os.mkdir(path)

                # Because this dir is a nested one, needs os.makedirs unlike the others
                if not os.path.isdir(bundledOverridePath):

                    os.makedirs(bundledOverridePath)

                # Step 5: Copy each mod into the backup folder
                for mod in (x for x in mods):

                    self.cancelCheck()

                    self.setCurrentProgress.emit(1, f'Copying {mod} to {BACKUP_MODS}')

                    modType = self.saveManager.getType(mod)

                    # In the case this file is not a mod
                    if modType is None:
                        logging.warning('File %s is not a mod or does not have an entry in %s. Skipping...', mod, MOD_CONFIG)
                        continue

                    # If the mod is disabled then the src will go to the disabled mods directory
                    src = os.path.join(srcPathDict[modType], mod) if self.saveManager.getEnabled(mod) else os.path.join(disPath, mod)

                    output = os.path.join(outputPathDict[modType], mod)

                    # shutil.copytree() can't overwrite files, so if it already exists it must be deleted first
                    if os.path.exists(output):

                        logging.info('%s already exists within the backup, overwriting...', mod)

                        shutil.rmtree(output)

                    shutil.copytree(src, output)
                
                self.cancelCheck()

                # Step 6: Zip Backup folder
                self.setCurrentProgress.emit(1, f'Zipping to {bundledFilePath}\nThis might take some time...')

                # Create Zip, this should overwrite if it already exists
                shutil.make_archive(BACKUP_MODS, 'zip', bundledFilePath)

                # Step 7: Cleanup

                self.setCurrentProgress.emit(1, 'Cleanup')

                # Delete Folder
                shutil.rmtree(bundledFilePath)

                self.succeeded.emit()

            except Exception as e:

                # If something goes wrong, delete the unfinished bundled file
                if os.path.exists(bundledFilePath):
                    shutil.rmtree(bundledFilePath)

                if not self.cancel:
                    logging.error('Something went wrong in FileSaver.backupMods():\n%s', str(e))
                    self.error.emit(f'Something went wrong in FileSaver.backupMods():\n{e}')
                
                    self.cancel = True
