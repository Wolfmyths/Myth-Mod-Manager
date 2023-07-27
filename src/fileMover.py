import shutil
import os

from save import Save, OptionsManager
import errorChecking
from constant_vars import MOD_TYPE, TYPE_MODS, OPTIONS_GAMEPATH, OPTIONS_DISPATH, OPTIONS_SECTION, MODS_DISABLED_PATH_DEFAULT, MOD_LIST_OBJECT, MOD_OVERRIDE_LIST_OBJECT, TYPE_MODS_OVERRIDE, BACKUP_MODS, MODSIGNORE

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

        gamePath = self.optionsManager.get(OPTIONS_SECTION, OPTIONS_GAMEPATH, fallback='')

        disabledModsPath = self.optionsManager.get(OPTIONS_SECTION, OPTIONS_DISPATH, fallback=MODS_DISABLED_PATH_DEFAULT)

        if not errorChecking.validDefaultDisabledModsPath():
            os.mkdir(disabledModsPath)

        # Checking if the mod is already in the disabled mods folder
        if not mod in os.listdir(disabledModsPath):

            if self.saveManager.getType(mod) == TYPE_MODS:

                modPath = os.path.join(gamePath, 'mods', mod)
            
            else:

                modPath = os.path.join(gamePath, 'assets', 'mod_overrides', mod)

            shutil.move(modPath, disabledModsPath)

    def moveToEnableModDir(self, mod: str) -> None:
        '''Returns a mod to their respective directory'''

        gamePath = self.optionsManager.get(OPTIONS_SECTION, OPTIONS_GAMEPATH, fallback='')

        disabledModsPath = self.optionsManager.get(OPTIONS_SECTION, OPTIONS_DISPATH, fallback=MODS_DISABLED_PATH_DEFAULT)

        if not errorChecking.validDefaultDisabledModsPath():
            os.mkdir(MODS_DISABLED_PATH_DEFAULT)

        if mod in os.listdir(disabledModsPath):

            if self.saveManager.getType(mod) == TYPE_MODS:

                modDestPath = os.path.join(gamePath, 'mods', mod)
            
            else:

                modDestPath = os.path.join(gamePath, 'assets', 'mod_overrides', mod)

            shutil.move(os.path.join(disabledModsPath, mod), modDestPath)
    
    def changeModType(self, mod: str , ChosenDir: None | str = None) -> None:
        '''
        Moves the mod to a new directory
        
        This function is used for the listWidget.py drag and drop events
        '''

        gamePath = self.optionsManager.get(OPTIONS_SECTION, OPTIONS_GAMEPATH, fallback='')
        modsDirPath = None


        if self.saveManager.getType(mod) == TYPE_MODS:

            modsDirPath = os.path.join(gamePath, 'mods')

            modDestPath = os.path.join(gamePath, 'assets', 'mod_overrides')
        
        elif self.saveManager.getType(mod) == TYPE_MODS_OVERRIDE:

            modsDirPath = os.path.join(gamePath, 'assets', 'mod_overrides')

            modDestPath = os.path.join(gamePath, 'mods')
        
        elif ChosenDir == MOD_LIST_OBJECT:

            modDestPath = os.path.join(gamePath, 'mods')

        elif ChosenDir == MOD_OVERRIDE_LIST_OBJECT:

            modDestPath = os.path.join(gamePath, 'assets', 'mod_overrides')
        
        else:
            return
        
        modPath = os.path.join(modsDirPath, mod) if modsDirPath is not None else mod

        shutil.move(modPath, modDestPath)
    
    def deleteMod(self, modName: str) -> None:
        '''Removes the mod from the user's computer'''

        enabled = self.saveManager.isEnabled(modName)

        type = self.saveManager.getType(modName) if enabled else 'disabled'

        disPath = self.optionsManager.get(OPTIONS_SECTION, OPTIONS_DISPATH, fallback=MODS_DISABLED_PATH_DEFAULT)

        gamePath = self.optionsManager.get(OPTIONS_SECTION, OPTIONS_GAMEPATH)

        pathDict = {TYPE_MODS_OVERRIDE : os.path.join(gamePath, 'assets', 'mod_overrides'), TYPE_MODS : os.path.join(gamePath, 'mods'), 'disabled' : disPath}

        self.saveManager.removeMods(modName)

        path = os.path.join(pathDict[type], modName)

        shutil.rmtree(path)
    
    def backupMods(self) -> int:
        '''
        Takes all of the mods and compresses them into a zip file, the output is in the exe directory

        Returns an exit code:

        0 = Failure,
        1 = Success
        '''

        gamePath = self.optionsManager.get(OPTIONS_SECTION, OPTIONS_GAMEPATH, fallback=None)

        disPath = self.optionsManager.get(OPTIONS_SECTION, OPTIONS_DISPATH, fallback=MODS_DISABLED_PATH_DEFAULT)

        modPath = os.path.join(gamePath, 'mods')

        mod_overridePath = os.path.join(gamePath, 'assets', 'mod_overrides')

        bundledFilePath = os.path.join(os.path.abspath(os.curdir), BACKUP_MODS)

        bundledModsPath = os.path.join(bundledFilePath, 'mods')
        
        bundledOverridePath = os.path.join(bundledFilePath, 'assets', 'mod_overrides')

        outputPathDict = {TYPE_MODS_OVERRIDE : os.path.join(bundledFilePath, 'assets', 'mod_overrides'), TYPE_MODS : os.path.join(bundledFilePath, 'mods')}

        srcPathDict = {TYPE_MODS_OVERRIDE : mod_overridePath, TYPE_MODS : modPath}

        try:

            # Make folders
            # Backup folder
            if not os.path.exists(bundledFilePath):

                os.mkdir(bundledFilePath)

            # /mods
            if not os.path.exists(bundledModsPath):

                os.mkdir(bundledModsPath)

            # /assets/mod_overrides
            if not os.path.exists(bundledOverridePath):

                os.makedirs(bundledOverridePath)

            # Every mod
            mods = list([x for x in os.listdir(modPath) if x not in MODSIGNORE] + os.listdir(mod_overridePath) + os.listdir(disPath))

            for mod in mods:

                modType = self.saveManager.get(mod, MOD_TYPE)

                # If the mod is disabled then the src will go to the disabled mods directory
                src = os.path.join(srcPathDict[modType], mod) if self.saveManager.isEnabled(mod) else os.path.join(disPath, mod)

                output = os.path.join(outputPathDict[modType], mod)

                # shutil.copytree() can't overwrite files, so if it already exists it must be deleted first
                if os.path.exists(output):

                    shutil.rmtree(output)

                shutil.copytree(src, output)
            
            # Create Zip, this should overwrite if it already exists
            shutil.make_archive(BACKUP_MODS, 'zip', bundledFilePath)

            # Delete Folder
            shutil.rmtree(bundledFilePath)

            return 1
            
        except Exception as e:

            print(e)

            # If something goes wrong, delete the unfinished bundled file
            if os.path.exists(bundledFilePath):
                shutil.rmtree(bundledFilePath)
            
            return 0


    def createDisabledModFolder(self) -> None:

        path = self.optionsManager.get(OPTIONS_SECTION, OPTIONS_DISPATH, fallback=MODS_DISABLED_PATH_DEFAULT)

        if not os.path.exists(path):

            try:

                os.mkdir(path)

            except FileNotFoundError:

                os.mkdir(MODS_DISABLED_PATH_DEFAULT)