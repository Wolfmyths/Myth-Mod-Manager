
import os
import subprocess

import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt as qt

from widgets.tableWidget import ModListWidget
from save import Save, OptionsManager
import errorChecking
from constant_vars import TYPE_MODS, TYPE_MODS_OVERRIDE, OPTIONS_GAMEPATH, START_PAYDAY_PATH, MOD_TABLE_OBJECT

class ModManager(qtw.QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.saveManager = Save()
        self.optionsManager = OptionsManager()

        layout = qtw.QVBoxLayout()

        self.setAcceptDrops(True)

        self.refresh = qtw.QPushButton('Refresh Mods', self)
        self.refresh.clicked.connect(lambda: self.modsTable.refreshMods())

        self.openGameDir = qtw.QPushButton('Open Game Directory', self)
        self.openGameDir.clicked.connect(lambda: os.startfile(self.optionsManager.getOption(OPTIONS_GAMEPATH)))

        self.startGame = qtw.QPushButton('Start PAYDAY 2', self)
        self.startGame.clicked.connect(lambda: self.startPayday())

        self.modLabel = qtw.QLabel(self)

        self.search = qtw.QLineEdit()
        self.search.setPlaceholderText('Search...')
        self.search.textChanged.connect(lambda x: self.modsTable.search(x))

        self.modsTable = ModListWidget()
        self.modsTable.itemChanged.connect(lambda: self.modLabel.setText(
            f'''
            Total Mods: {self.modsTable.rowCount()}
            Mods: {self.modsTable.getModTypeCount(TYPE_MODS)}
            Mod_Overrides: {self.modsTable.getModTypeCount(TYPE_MODS_OVERRIDE)}
            '''))
        
        self.modsTable.setObjectName(MOD_TABLE_OBJECT)

        self.modsTable.refreshMods()


        for widget in (self.refresh, self.openGameDir, self.startGame, self.modLabel, self.search, self.modsTable):
            layout.addWidget(widget)

        self.setLayout(layout)
    
    def startPayday(self):

        if errorChecking.validGamePath():

            gamePath = self.optionsManager.getOption(OPTIONS_GAMEPATH)

            drive = gamePath[0].lower()

            # Starts START_PAYDAY.bat
            # First argument is to change the directory to the game's directory
            # Second argument the drive for the cd command
            # Third argument is the exe name
            subprocess.call([START_PAYDAY_PATH, gamePath, drive, 'payday2_win32_release.exe'])