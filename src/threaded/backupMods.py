import os
import shutil
import logging

from threaded.file_mover import FileMover
from constant_vars import ModType, OPTIONS_DISPATH, MODS_DISABLED_PATH_DEFAULT, BACKUP_MODS, MODSIGNORE, MOD_TYPE

class BackupMods(FileMover):
    def run(self) -> None:
        self.backupMods()
        return super().run()

    def backupMods(self) -> None:
            '''Takes all of the mods and compresses them into a zip file, the output is in the exe directory'''

            # Step 1: Gather Options

            disPath = self.optionsManager.getOption(OPTIONS_DISPATH, fallback=MODS_DISABLED_PATH_DEFAULT)

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

            taskCanceledError = 'Task was canceled'

            try:

                # Step 4: Create Folders

                # Every mod
                mods = list([x for x in os.listdir(modPath) if x not in MODSIGNORE] + os.listdir(mod_overridePath) + os.listdir(disPath) + os.listdir(maps_path))
                print(mods)

                self.setTotalProgress.emit(len(mods) + 3) # Add 3 for the extra steps that aren't the list length

                self.setCurrentProgress.emit(1, f'Validating backup folder paths')

                # Creating backup environment
                for path in (bundledFilePath, bundledModsPath, bundledMapsPath):

                    if not os.path.exists(path):

                        os.mkdir(path)

                # Because this dir is a nested one, needs os.makedirs unlike the others
                if not os.path.exists(bundledOverridePath):

                    os.makedirs(bundledOverridePath)

                # Step 5: Copy each mod into the backup folder
                for mod in (x for x in mods):

                    if self.cancel: raise Exception(taskCanceledError)

                    self.setCurrentProgress.emit(1, f'Copying {mod} to {BACKUP_MODS}')

                    modType = self.saveManager.getType(mod)

                    # If the mod is disabled then the src will go to the disabled mods directory
                    src = os.path.join(srcPathDict[modType], mod) if self.saveManager.isEnabled(mod) else os.path.join(disPath, mod)

                    output = os.path.join(outputPathDict[modType], mod)

                    # shutil.copytree() can't overwrite files, so if it already exists it must be deleted first
                    if os.path.exists(output):

                        logging.info('%s already exists within the backup, overwriting...', mod)

                        shutil.rmtree(output)

                    shutil.copytree(src, output)
                
                if self.cancel: raise Exception(taskCanceledError)

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
                    self.error.emit(str(e))