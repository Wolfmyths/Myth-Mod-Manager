
import os
import subprocess

import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt as qt

from widgets.tableWidget import ModListWidget
from save import Save, OptionsManager
import errorChecking
from constant_vars import MODSIGNORE, TYPE_MODS, TYPE_MODS_OVERRIDE, OPTIONS_GAMEPATH, OPTIONS_DISPATH, MOD_ENABLED, MOD_TYPE, MODS_DISABLED_PATH_DEFAULT, START_PAYDAY_PATH, MOD_TABLE_OBJECT

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
        self.openGameDir.clicked.connect(lambda: os.startfile(self.optionsManager.getOption(OPTIONS_GAMEPATH)))

        self.startGame = qtw.QPushButton('Start PAYDAY 2', self)
        self.startGame.clicked.connect(lambda: self.startPayday())

        self.modLabel = qtw.QLabel(self)

        self.search = qtw.QLineEdit()
        self.search.setPlaceholderText('Search...')
        self.search.textChanged.connect(lambda: self.modsTable.keyboardSearch(self.search.text()))

        self.modsTable = ModListWidget()
        self.modsTable.itemChanged.connect(lambda: self.modLabel.setText(
            f'''
            Total Mods: {self.modsTable.rowCount()}
            Mods: {self.modsTable.getModTypeCount(TYPE_MODS)}
            Mod_Overrides: {self.modsTable.getModTypeCount(TYPE_MODS_OVERRIDE)}
            '''))
        
        self.modsTable.setObjectName(MOD_TABLE_OBJECT)

        self.refreshMods()


        for widget in (self.refresh, self.openGameDir, self.startGame, self.modLabel, self.search, self.modsTable):
            layout.addWidget(widget)

        self.setLayout(layout)

    def refreshMods(self) -> None:
        '''Refreshes the mod lists in the manager'''

        if self.modsTable.rowCount() > 0:
            for i in range(0, self.modsTable.rowCount() + 1):
                self.modsTable.removeRow(i)

        # Gather mods from directories
        mods = self.getMods()

        # Save mods into .ini
        self.saveManager.addMods((mods[0], TYPE_MODS_OVERRIDE), (mods[1], TYPE_MODS))

        # Just incase disabled folder doesn't exist
        errorChecking.createDisabledModFolder()

        disModFolder = self.optionsManager.getOption(OPTIONS_DISPATH)
        disModFolderContents = os.listdir(disModFolder)

        # Add mods to the table widget
        for mod in (x for x in mods[0] + mods[1]):

            type = self.saveManager.getType(mod)
            isDisabled = mod in disModFolderContents

            if isDisabled:
                self.saveManager[mod][MOD_ENABLED] = 'False'
                enabled = 'Disabled'
            else:
                self.saveManager[mod][MOD_ENABLED] = 'True'
                enabled = 'Enabled'

            self.modsTable.addMod(name=mod, type=type, enabled=enabled)
        
        # Save changes
        self.saveManager.writeData()

        # Clear selections from the disabled mod check
        self.modsTable.clearSelection()

        self.modsTable.sort()

    def getMods(self) -> list[list[str]]:
        '''
        Returns a list of two lists that have all of the mods from 
        "\\mods" and "\\assets\\mod_overrides"

        Index 0 is "\\assets\\mod_overrides", index 1 is "\\mods"
        '''

        mod_override: list[str] = []
        mods: list[str] = []

        gamePath = self.optionsManager.getOption(OPTIONS_GAMEPATH, fallback='')

        modsPath = os.path.join(gamePath, 'mods')

        mod_overridePath = os.path.join(gamePath, 'assets', 'mod_overrides')

        disabledModsPath = self.optionsManager.getOption(OPTIONS_DISPATH, fallback=MODS_DISABLED_PATH_DEFAULT)

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

        return [mod_override, mods]
    
    def startPayday(self):

        if errorChecking.validGamePath():

            gamePath = self.optionsManager.getOption(OPTIONS_GAMEPATH)

            drive = gamePath[0].lower()

            # Starts START_PAYDAY.bat
            # First argument is to change the directory to the game's directory
            # Second argument the drive for the cd command
            # Third argument is the exe name
            subprocess.call([START_PAYDAY_PATH, gamePath, drive, 'payday2_win32_release.exe'])