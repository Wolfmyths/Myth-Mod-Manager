import shutil
import os

from PySide6.QtCore import QThread, Signal, QUrl

from save import Save, OptionsManager
from widgets.announcementQDialog import Notice
from widgets.newModQDialog import newModLocation
import errorChecking
from constant_vars import MOD_TYPE, TYPE_MODS, OPTIONS_GAMEPATH, OPTIONS_DISPATH, MODS_DISABLED_PATH_DEFAULT, TYPE_MODS_OVERRIDE, BACKUP_MODS, MODSIGNORE


class FileMover(QThread):
    '''
    File Manager of the program.

    Any function that involves moving files goes here.

    !IMPORTANT!
    
    Should usually not be ran by itself, please use `progress()` from `widgets.progressWidget`
    or something similar

    This allows it to properly thread and use the class' signals for the `QProgressBar`

    The mode parameter is to choose which function you want (Since it needs to be
    wrapped in `run()`)

    Possible parameters:
    
    + 0 : moveToDisabledDir(*mods: str)
    + 1 : moveToEnableModDir(*mods: str)
    + 2 : changeModType(*mods: str | QUrl)
    + 3 : unZipMod(tuple[str, str])
    + 4 : deleteMod(modName: str)
    + 5 : backupMods()
    '''

    setTotalProgress = Signal(int)

    setCurrentProgress = Signal(int, str)

    succeeded = Signal()

    error = Signal(str)

    cancel = False

    def __init__(self, mode: int, *args):
        super().__init__()

        self.mode = mode

        self.args = args

        self.saveManager = Save()
        self.optionsManager = OptionsManager()

        self.modeDict = {0 : lambda: self.moveToDisabledDir(*args),
                         1 : lambda: self.moveToEnableModDir(*args),
                         2 : lambda: self.changeModType(*args),
                         3 : lambda: self.unZipMod(*args),
                         4 : lambda: self.deleteMod(*args),
                         5 : self.backupMods}
    
    def run(self) -> None:

        self.modeDict[self.mode]()

        return super().run()

    def moveToDisabledDir(self, *mods: str) -> None:
        '''Moves a mod to the disabled folder'''

        self.setTotalProgress.emit(len(mods))

        gamePath = self.optionsManager.getOption(OPTIONS_GAMEPATH, fallback='')

        disabledModsPath = self.optionsManager.getOption(OPTIONS_DISPATH, fallback=MODS_DISABLED_PATH_DEFAULT)

        errorChecking.createDisabledModFolder()

        for mod in mods:

            if self.cancel: break

            self.setCurrentProgress.emit(1, f'Disabling {mod}')

            # Checking if the mod is already in the disabled mods folder
            if not mod in os.listdir(disabledModsPath):

                if self.saveManager.getType(mod) == TYPE_MODS:

                    modPath = os.path.join(gamePath, 'mods', mod)
                
                else:

                    modPath = os.path.join(gamePath, 'assets', 'mod_overrides', mod)

                shutil.move(modPath, disabledModsPath)
        
        self.succeeded.emit()

    def moveToEnableModDir(self, *mods: str) -> None:
        '''Returns a mod to their respective directory'''

        self.setTotalProgress.emit(len(mods))

        gamePath = self.optionsManager.getOption(OPTIONS_GAMEPATH, fallback='')

        disabledModsPath = self.optionsManager.getOption(OPTIONS_DISPATH, fallback=MODS_DISABLED_PATH_DEFAULT)

        errorChecking.createDisabledModFolder()

        for mod in mods:

            if self.cancel: break

            self.setCurrentProgress.emit(1, f'Enabling {mod}')

            if mod in os.listdir(disabledModsPath):

                if self.saveManager.getType(mod) == TYPE_MODS:

                    modDestPath = os.path.join(gamePath, 'mods', mod)
                
                else:

                    modDestPath = os.path.join(gamePath, 'assets', 'mod_overrides', mod)

                shutil.move(os.path.join(disabledModsPath, mod), modDestPath)
        
        self.succeeded.emit()
    
    def changeModType(self, *mods: tuple[QUrl, str] | str) -> None:
        '''
        Moves the mod to a new directory

        If the arg is going to be a URL to a folder, convert into a QURL first.
        '''

        self.setTotalProgress.emit(len(mods))

        gamePath = self.optionsManager.getOption(OPTIONS_GAMEPATH, fallback='')

        ChosenDir = None

        pathDict = {TYPE_MODS : os.path.join(gamePath, 'mods'), TYPE_MODS_OVERRIDE : os.path.join(gamePath, 'assets', 'mod_overrides')}

        
        for mod in mods:
            
            # If the current set of args are URLs to folders
            if type(mod) == tuple:

                modURL = mod[0]
                ChosenDir = mod[1]
                
                modsDirPath = modURL.toLocalFile()

                mod = modURL.fileName()

            self.setCurrentProgress.emit(1, f'Installing {mod}')

            # Setting the destination and mod directory paths
            # If the mod is a URL to a folder then we don't need set a mod directory path
            if ChosenDir == TYPE_MODS:

                modDestPath = pathDict[TYPE_MODS]

            elif ChosenDir == TYPE_MODS_OVERRIDE:

                modDestPath = pathDict[TYPE_MODS_OVERRIDE]

            elif self.saveManager.getType(mod) == TYPE_MODS:

                modsDirPath = pathDict[TYPE_MODS]

                modDestPath = pathDict[TYPE_MODS_OVERRIDE]
            
            elif self.saveManager.getType(mod) == TYPE_MODS_OVERRIDE:

                modsDirPath = pathDict[TYPE_MODS_OVERRIDE]

                modDestPath = pathDict[TYPE_MODS]
            
            else:
                continue

            modPath = os.path.join(modsDirPath, mod) if ChosenDir is None else modsDirPath
            print(modPath)
            print(modDestPath)

            doesPathAlreadyExist = os.path.exists(os.path.join(modDestPath, mod))

            if not doesPathAlreadyExist:
                shutil.move(modPath, modDestPath)
        
        self.succeeded.emit()

    def unZipMod(self, *mods: tuple[QUrl, str]) -> None:
        '''Asks the user where each mod will go and then unzips it to that directory'''

        self.setTotalProgress.emit(len(mods))

        print(mods)

        try:

            for modURL in mods:

                url = modURL[0]

                src = url.toLocalFile()

                mod = url.fileName()

                type = modURL[1]

                if self.cancel: break

                self.setCurrentProgress.emit(1, f"Unpacking {mod}")

                if os.path.exists(src):

                        gamepath = self.optionsManager.getOption(OPTIONS_GAMEPATH)

                        destPathDict = {TYPE_MODS : os.path.join(gamepath, 'mods'), TYPE_MODS_OVERRIDE : os.path.join(gamepath, 'assets', 'mod_overrides')}

                        if src.endswith('.rar'):

                            notice = Notice(headline='.rar not supported :(', message=
                                            f"""
                                            Mod Effected: {mod}
                                            The .rar file format is not supported.
                                            You can open the .rar and drag the mod from there.

                                            Click OK to continue unzipping and installing the remaining mods.
                                            """)
                            notice.exec()

                            continue

                        shutil.unpack_archive(src, destPathDict[type])

        except Exception as e:

            self.error.emit(str(e))
        
        self.succeeded.emit()
    
    def deleteMod(self, *mods: str) -> None:
        '''Removes the mod(s) from the user's computer'''

        self.setTotalProgress.emit(len(mods))

        disPath = self.optionsManager.getOption(OPTIONS_DISPATH, fallback=MODS_DISABLED_PATH_DEFAULT)

        gamePath = self.optionsManager.getOption(OPTIONS_GAMEPATH)

        pathDict = {TYPE_MODS_OVERRIDE : os.path.join(gamePath, 'assets', 'mod_overrides'), TYPE_MODS : os.path.join(gamePath, 'mods'), 'disabled' : disPath}

        for modName in mods:

            if self.cancel: break

            self.setCurrentProgress.emit(1, f'Deleting {modName}')

            enabled = self.saveManager.isEnabled(modName)

            type = self.saveManager.getType(modName) if enabled else 'disabled'

            self.saveManager.removeMods(modName)

            path = os.path.join(pathDict[type], modName)

            if os.path.exists(path):
                shutil.rmtree(path)

        self.succeeded.emit()

    def backupMods(self) -> None:
        '''Takes all of the mods and compresses them into a zip file, the output is in the exe directory'''

        # Step 1: Gather Options

        gamePath = self.optionsManager.getOption(OPTIONS_GAMEPATH)

        disPath = self.optionsManager.getOption(OPTIONS_DISPATH, fallback=MODS_DISABLED_PATH_DEFAULT)

        # Step 2: Set Paths

        modPath = os.path.join(gamePath, 'mods')

        mod_overridePath = os.path.join(gamePath, 'assets', 'mod_overrides')

        bundledFilePath = os.path.join(os.path.abspath(os.curdir), BACKUP_MODS)

        bundledModsPath = os.path.join(bundledFilePath, 'mods')
        
        bundledOverridePath = os.path.join(bundledFilePath, 'assets', 'mod_overrides')

        outputPathDict = {TYPE_MODS_OVERRIDE : os.path.join(bundledFilePath, 'assets', 'mod_overrides'), TYPE_MODS : os.path.join(bundledFilePath, 'mods')}

        srcPathDict = {TYPE_MODS_OVERRIDE : mod_overridePath, TYPE_MODS : modPath}

        try:
            
            # Step 4: Create Folders

            # Every mod
            mods = list([x for x in os.listdir(modPath) if x not in MODSIGNORE] + os.listdir(mod_overridePath) + os.listdir(disPath))

            self.setTotalProgress.emit(len(mods) + 3) # Add 3 for the extra steps that aren't the list lengeth

            self.setCurrentProgress.emit(1, f'Validating backup folder paths')
            # Backup folder
            if not os.path.exists(bundledFilePath):

                os.mkdir(bundledFilePath)

            # /mods
            if not os.path.exists(bundledModsPath):

                os.mkdir(bundledModsPath)

            # /assets/mod_overrides
            if not os.path.exists(bundledOverridePath):

                os.makedirs(bundledOverridePath)

            # Step 5: Copy each mod into the backup folder
            for mod in (x for x in mods):

                if self.cancel: raise Exception('Task was canceled')

                self.setCurrentProgress.emit(1, f'Copying {mod} to {BACKUP_MODS}')

                modType = self.saveManager.get(mod, MOD_TYPE)

                # If the mod is disabled then the src will go to the disabled mods directory
                src = os.path.join(srcPathDict[modType], mod) if self.saveManager.isEnabled(mod) else os.path.join(disPath, mod)

                output = os.path.join(outputPathDict[modType], mod)

                # shutil.copytree() can't overwrite files, so if it already exists it must be deleted first
                if os.path.exists(output):

                    shutil.rmtree(output)

                shutil.copytree(src, output)
            
            # Step 6: Zip Backup folder
            self.setCurrentProgress.emit(1, f'Zipping to {bundledFilePath}')
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
                self.error.emit(str(e))
