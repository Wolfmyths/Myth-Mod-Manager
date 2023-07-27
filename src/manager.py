
import os
import subprocess

import PySide6.QtWidgets as qtw

from widgets.listWidget import ModListWidget
from save import Save, OptionsManager
import errorChecking
from constant_vars import MODSIGNORE, TYPE_MODS, TYPE_MODS_OVERRIDE, OPTIONS_SECTION, OPTIONS_GAMEPATH, OPTIONS_DISPATH, MOD_ENABLED, MOD_TYPE, MODS_DISABLED_PATH_DEFAULT, START_PAYDAY_PATH, MOD_LIST_OBJECT, MOD_OVERRIDE_LIST_OBJECT

class ModManager(qtw.QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.saveManager = Save()
        self.optionsManager = OptionsManager()

        layout = qtw.QVBoxLayout()

        self.setAcceptDrops(True)

        self.refresh = qtw.QPushButton('Refresh Mods', self)
        self.refresh.clicked.connect(lambda: self.refreshMods())

        self.openGameDir = qtw.QPushButton('Open Game Directory', self)
        self.openGameDir.clicked.connect(lambda: os.startfile(self.optionsManager.get(OPTIONS_SECTION, OPTIONS_GAMEPATH)))

        self.startGame = qtw.QPushButton('Start PAYDAY 2', self)
        self.startGame.clicked.connect(lambda: self.startPayday())

        self.overrideLabel = qtw.QLabel(self)

        self.override = ModListWidget()
        self.override.setObjectName(MOD_OVERRIDE_LIST_OBJECT)

        self.modLabel = qtw.QLabel(self)

        self.mods = ModListWidget()
        self.mods.setObjectName(MOD_LIST_OBJECT)

        self.refreshMods()


        for widget in (self.refresh, self.openGameDir, self.startGame, self.overrideLabel, self.override, self.modLabel, self.mods):
            layout.addWidget(widget)

        self.setLayout(layout)

    def refreshMods(self) -> None:
        '''Refreshes the mod lists in the manager'''

        # Clear lists if needed
        if self.override.count() > 0:
            self.override.clear()

        if self.mods.count() > 0:
            self.mods.clear()

        # Gather mods from directories
        mods = self.getMods()

        # Add mods from their respective dirs into the right list
        self.override.addItems(mods[0])
        self.mods.addItems(mods[1])

        # Save mods into .ini
        self.saveManager.addMods((mods[0], TYPE_MODS_OVERRIDE), (mods[1], TYPE_MODS))

        self.overrideLabel.setText(f'{TYPE_MODS_OVERRIDE}: {self.override.count()} Mods Installed')

        self.modLabel.setText(f'{TYPE_MODS}: {self.mods.count()} Mods Installed')

        # Show which mods are disabled in each list

        # Checking if each mod is disabled
        for list in mods:

            for index, key in enumerate(list):

                self.checkMod(index, key)

        # Clear selections from the disabled mod check
        self.mods.clearSelection()
        self.override.clearSelection()
    
    def checkMod(self, index: int, key: str):

        if not errorChecking.validDefaultDisabledModsPath():
            os.mkdir(MODS_DISABLED_PATH_DEFAULT)

        disabledMods = os.listdir(self.optionsManager.get(OPTIONS_SECTION, OPTIONS_DISPATH, fallback=MODS_DISABLED_PATH_DEFAULT))

        if self.saveManager.has_section(key) and key in disabledMods:

            self.saveManager[key][MOD_ENABLED] = 'False'

        if not self.saveManager.isEnabled(key):

            # setItemDisabled() disables the currently selected item
            # so an item needs to be selected first

            if self.saveManager.getType(key) == TYPE_MODS:

                self.mods.setCurrentRow(index)
                self.mods.setItemNameDisabled(self.mods.item(index))
            
            else:

                self.override.setCurrentRow(index)
                self.override.setItemNameDisabled(self.override.item(index))

    def getMods(self) -> list[list[str]]:
        '''
        Returns a list of two lists that have all of the mods from 
        "\\mods" and "\\assets\\mod_overrides"

        Index 0 is "\\assets\\mod_overrides", index 1 is "\\mods"
        '''

        mod_override: list[str] = []
        mods: list[str] = []

        gamePath = self.optionsManager.get(OPTIONS_SECTION, OPTIONS_GAMEPATH, fallback='')

        modsPath = os.path.join(gamePath, 'mods')

        mod_overridePath = os.path.join(gamePath, 'assets', 'mod_overrides')

        disabledModsPath = self.optionsManager.get(OPTIONS_SECTION, OPTIONS_DISPATH, fallback=MODS_DISABLED_PATH_DEFAULT)

        # Mods Folder
        if os.path.exists(modsPath):

            for mod in os.listdir(modsPath):

                modPath = os.path.join(modsPath, mod)

                if mod not in MODSIGNORE and errorChecking.getFileType(modPath) == 'dir':
                    
                    mods.append(mod)

        # mod_override Folder
        if os.path.exists(mod_overridePath):

            for mod in os.listdir(mod_overridePath):

                modPath = os.path.join(mod_overridePath, mod)

                if errorChecking.getFileType(modPath) == 'dir':

                    mod_override.append(mod)

        # Disabled Mods Folder
        if os.path.exists(disabledModsPath):
            
            for mod in os.listdir(disabledModsPath):

                if self.saveManager.has_section(mod):
                    
                    if self.saveManager[mod][MOD_TYPE] == TYPE_MODS:

                        mods.append(mod)
                    
                    elif self.saveManager[mod][MOD_TYPE] == TYPE_MODS_OVERRIDE:

                        mod_override.append(mod)
        
        # Sort lists because the disabled mods folder for loop makes them unsorted
        mod_override = sorted(mod_override)
        mods = sorted(mods)

        return [mod_override, mods]
    
    def startPayday(self):

        if errorChecking.validGamePath():

            gamePath = self.optionsManager.get(OPTIONS_SECTION, OPTIONS_GAMEPATH)

            drive = gamePath[0].lower()

            # Starts START_PAYDAY.bat
            # First argument is to change the directory to the game's directory
            # Second argument the drive for the cd command
            # Third argument is the exe name
            subprocess.call([START_PAYDAY_PATH, gamePath, drive, 'payday2_win32_release.exe'])