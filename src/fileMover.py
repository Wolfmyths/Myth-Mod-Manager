import shutil
import os

from save import Save, OptionsManager
from constant_vars import MOD_TYPE, TYPE_MODS, OPTIONS_GAMEPATH, OPTIONS_DISPATH, OPTIONS_SECTION, MODS_DISABLED_PATH_DEFAULT, MOD_LIST_OBJECT, MOD_OVERRIDE_LIST_OBJECT, TYPE_MODS_OVERRIDE

class FileMover():
    def __init__(self):

        self.saveManager = Save()
        self.optionsManager = OptionsManager()

    def moveToDisabledDir(self, mod: str) -> None:
        '''Moves a mod to the disabled folder'''

        gamePath = self.optionsManager.get(OPTIONS_SECTION, OPTIONS_GAMEPATH, fallback='')

        disabledModsPath = self.optionsManager.get(OPTIONS_SECTION, OPTIONS_DISPATH, fallback=MODS_DISABLED_PATH_DEFAULT)

        # Checking if the mod is already in the disabled mods folder
        if not mod in os.listdir(disabledModsPath):

            if self.saveManager.get(mod, MOD_TYPE) == TYPE_MODS:

                modPath = os.path.join(gamePath, 'mods', mod)
            
            else:

                modPath = os.path.join(gamePath, 'assets', 'mod_overrides', mod)

            shutil.move(modPath, disabledModsPath)

    def moveToEnableModDir(self, mod: str) -> None:
        '''Returns a mod to their respective directory'''

        gamePath = self.optionsManager.get(OPTIONS_SECTION, OPTIONS_GAMEPATH, fallback='')

        disabledModsPath = self.optionsManager.get(OPTIONS_SECTION, OPTIONS_DISPATH, fallback=MODS_DISABLED_PATH_DEFAULT)

        if mod in os.listdir(disabledModsPath):

            if self.saveManager.get(mod, MOD_TYPE) == TYPE_MODS:

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


        if self.saveManager.get(mod, MOD_TYPE, fallback=None) == TYPE_MODS:

            modsDirPath = os.path.join(gamePath, 'mods')

            modDestPath = os.path.join(gamePath, 'assets', 'mod_overrides')
        
        elif self.saveManager.get(mod, MOD_TYPE, fallback=None) == TYPE_MODS_OVERRIDE:

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

        type = self.saveManager.get(modName, MOD_TYPE)

        gamePath = self.optionsManager.get(OPTIONS_SECTION, OPTIONS_GAMEPATH)

        pathDict = {TYPE_MODS_OVERRIDE : os.path.join(gamePath, 'assets', 'mod_overrides'), TYPE_MODS : os.path.join(gamePath, 'mods')}

        self.saveManager.removeMods(modName)

        path = os.path.join(pathDict[type], modName)

        shutil.rmtree(path)