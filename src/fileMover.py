import shutil
import os
from zipfile import ZipFile

from save import Save, OptionsManager
from widgets.announcementQDialog import Notice
import errorChecking
from constant_vars import MOD_TYPE, TYPE_MODS, OPTIONS_GAMEPATH, OPTIONS_DISPATH, MODS_DISABLED_PATH_DEFAULT, TYPE_MODS_OVERRIDE, BACKUP_MODS, MODSIGNORE

class FileMover():
    '''
    File Manager of the program.

    Any function that involves moving files goes here.
    '''
    def __init__(self):

        self.saveManager = Save()
        self.optionsManager = OptionsManager()

    def moveToDisabledDir(self, mod: str) -> None:
        '''Moves a mod to the disabled folder'''

        gamePath = self.optionsManager.getOption(OPTIONS_GAMEPATH, fallback='')

        disabledModsPath = self.optionsManager.getOption(OPTIONS_DISPATH, fallback=MODS_DISABLED_PATH_DEFAULT)

        errorChecking.createDisabledModFolder()

        # Checking if the mod is already in the disabled mods folder
        if not mod in os.listdir(disabledModsPath):

            if self.saveManager.getType(mod) == TYPE_MODS:

                modPath = os.path.join(gamePath, 'mods', mod)
            
            else:

                modPath = os.path.join(gamePath, 'assets', 'mod_overrides', mod)

            shutil.move(modPath, disabledModsPath)

    def moveToEnableModDir(self, mod: str) -> None:
        '''Returns a mod to their respective directory'''

        gamePath = self.optionsManager.getOption(OPTIONS_GAMEPATH, fallback='')

        disabledModsPath = self.optionsManager.getOption(OPTIONS_DISPATH, fallback=MODS_DISABLED_PATH_DEFAULT)

        errorChecking.createDisabledModFolder()

        if mod in os.listdir(disabledModsPath):

            if self.saveManager.getType(mod) == TYPE_MODS:

                modDestPath = os.path.join(gamePath, 'mods', mod)
            
            else:

                modDestPath = os.path.join(gamePath, 'assets', 'mod_overrides', mod)

            shutil.move(os.path.join(disabledModsPath, mod), modDestPath)
    
    def changeModType(self, mod: str , ChosenDir: None | str = None) -> None:
        '''
        Moves the mod to a new directory

        The arg ChosenDir is used when a brand new mod is introduced,
        it must be one of the following types

        + TYPE_MODS
        + TYPE_MODS_OVERRIDE
        '''

        gamePath = self.optionsManager.getOption(OPTIONS_GAMEPATH, fallback='')
        modsDirPath = None

        pathDict = {TYPE_MODS : os.path.join(gamePath, 'mods'), TYPE_MODS_OVERRIDE : os.path.join(gamePath, 'assets', 'mod_overrides')}

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
            return
        
        modPath = os.path.join(modsDirPath, mod) if ChosenDir is None else mod

        if ChosenDir:
            doesPathAlreadyExist = os.path.exists(os.path.join(modDestPath, mod.split('/')[-1]))
            print(os.path.join(modDestPath, mod.split('/')[-1]))
        else:
            doesPathAlreadyExist = os.path.exists(os.path.join(modDestPath, mod))
            print(os.path.join(modDestPath, mod))

        if not doesPathAlreadyExist:
            shutil.move(modPath, modDestPath)
    
    def unZipMod(self, src: str, type: str) -> int | tuple[int, str]:
        '''
        Unzips a file to a specified directory
        
        Type arg needs to be one of the mod types like TYPE_MODS or TYPE_MODS_OVERRIDE
        otherwise it will result in a keyerror

        If a file was unzipped then it will return a tuple (exitcode, fileName)

        Exit Codes:
        + 0 : Error
        + 1 : Success
        + 2 : .rar is not supported
        '''

        if os.path.exists(src):

            try:

                gamepath = self.optionsManager.getOption(OPTIONS_GAMEPATH)

                destPathDict = {TYPE_MODS : os.path.join(gamepath, 'mods'), TYPE_MODS_OVERRIDE : os.path.join(gamepath, 'assets', 'mod_overrides')}

                fileName = None

                if src.endswith('.rar'):

                    notice = Notice(headline='.rar not supported :(', message="The .rar file format is not supported.\nYou can open the .rar and drag the mod from there.")
                    notice.exec()

                    exitCode = 2

                else:

                    # Find mod name (.zip version has other not needed info)
                    for info in ZipFile(src).infolist():

                        if info.is_dir():

                            fileName = info.filename.split('/')[0]

                    shutil.unpack_archive(src, destPathDict[type])

                    exitCode = 1

            except Exception as e:

                print(e)

                exitCode = 0

            finally:

                return exitCode if not fileName else exitCode, fileName
    
    def deleteMod(self, modName: str) -> None:
        '''Removes the mod from the user's computer'''

        enabled = self.saveManager.isEnabled(modName)

        type = self.saveManager.getType(modName) if enabled else 'disabled'

        disPath = self.optionsManager.getOption(OPTIONS_DISPATH, fallback=MODS_DISABLED_PATH_DEFAULT)

        gamePath = self.optionsManager.getOption(OPTIONS_GAMEPATH)

        pathDict = {TYPE_MODS_OVERRIDE : os.path.join(gamePath, 'assets', 'mod_overrides'), TYPE_MODS : os.path.join(gamePath, 'mods'), 'disabled' : disPath}

        self.saveManager.removeMods(modName)

        path = os.path.join(pathDict[type], modName)

        if os.path.exists(path):
            shutil.rmtree(path)
    
    def backupMods(self) -> int:
        '''
        Takes all of the mods and compresses them into a zip file, the output is in the exe directory

        Returns an exit code:

        0 = Failure,
        1 = Success
        '''

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

        # Step 3: Create Folders

        try:

            # Backup folder
            if not os.path.exists(bundledFilePath):

                os.mkdir(bundledFilePath)

            # /mods
            if not os.path.exists(bundledModsPath):

                os.mkdir(bundledModsPath)

            # /assets/mod_overrides
            if not os.path.exists(bundledOverridePath):

                os.makedirs(bundledOverridePath)
            
            # Step 4: Create a list of all the mods

            # Every mod
            mods = list([x for x in os.listdir(modPath) if x not in MODSIGNORE] + os.listdir(mod_overridePath) + os.listdir(disPath))

            # Step 5: Copy each mod into the backup folder
            for mod in (x for x in mods):

                modType = self.saveManager.get(mod, MOD_TYPE)

                # If the mod is disabled then the src will go to the disabled mods directory
                src = os.path.join(srcPathDict[modType], mod) if self.saveManager.isEnabled(mod) else os.path.join(disPath, mod)

                output = os.path.join(outputPathDict[modType], mod)

                # shutil.copytree() can't overwrite files, so if it already exists it must be deleted first
                if os.path.exists(output):

                    shutil.rmtree(output)

                shutil.copytree(src, output)
            
            # Step 6: Zip Backup folder

            # Create Zip, this should overwrite if it already exists
            shutil.make_archive(BACKUP_MODS, 'zip', bundledFilePath)

            # Step 7: Cleanup

            # Delete Folder
            shutil.rmtree(bundledFilePath)

            return 1
            
        except Exception as e:

            print(e)

            # If something goes wrong, delete the unfinished bundled file
            if os.path.exists(bundledFilePath):
                shutil.rmtree(bundledFilePath)
            
            return 0