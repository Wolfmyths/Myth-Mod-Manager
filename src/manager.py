import os
import subprocess
import logging
import PySide6.QtGui

import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt as qt
import PySide6.QtGui as qtg

from widgets.tableWidget import ModListWidget
from widgets.announcementQDialog import Notice
from save import Save, OptionsManager
import errorChecking
from constant_vars import TYPE_MODS, TYPE_MODS_OVERRIDE, OPTIONS_GAMEPATH, START_PAYDAY_PATH, MOD_TABLE_OBJECT, TYPE_MAPS

class ModManager(qtw.QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setObjectName('manager')
        selectAllShortCut = qtg.QShortcut(qtg.QKeySequence("Ctrl+A"), self)
        selectAllShortCut.activated.connect(lambda: self.modsTable.selectAll())

        deselectAllShortCut = qtg.QShortcut(qtg.QKeySequence("Ctrl+D"), self)
        deselectAllShortCut.activated.connect(lambda: self.deselectAllShortcut())

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

        modLabelLayout = qtw.QHBoxLayout()
        modLabelLayout.setSpacing(100)
        modLabelLayout.setAlignment(qt.AlignmentFlag.AlignHCenter)

        self.labelFrame = qtw.QFrame()

        self.totalModsLabel = qtw.QLabel(self)

        self.modsLabel = qtw.QLabel(self)

        self.overrideLabel = qtw.QLabel(self)

        self.mapsLabel = qtw.QLabel(self)

        for widget in (self.totalModsLabel, self.modsLabel, self.overrideLabel, self.mapsLabel):
            modLabelLayout.addWidget(widget)

        self.labelFrame.setLayout(modLabelLayout)

        self.search = qtw.QLineEdit()
        self.search.setPlaceholderText('Search...')
        self.search.textChanged.connect(lambda x: self.modsTable.search(x))

        self.modsTable = ModListWidget()
        self.modsTable.itemChanged.connect(lambda: self.updateModCount())
        
        self.modsTable.setObjectName(MOD_TABLE_OBJECT)

        self.modsTable.refreshMods()

        for widget in (self.refresh, self.openGameDir, self.startGame, self.labelFrame, self.search, self.modsTable):
            layout.addWidget(widget)

        self.setLayout(layout)
    
    def updateModCount(self):

        self.totalModsLabel.setText(f'Total Mods: {self.modsTable.rowCount()}')

        self.modsLabel.setText(f'Mods: {self.modsTable.getModTypeCount(TYPE_MODS)}')

        self.overrideLabel.setText(f'Mod_Overrides: {self.modsTable.getModTypeCount(TYPE_MODS_OVERRIDE)}')

        self.mapsLabel.setText(f'Maps: {self.modsTable.getModTypeCount(TYPE_MAPS)}')

    def startPayday(self):

        if errorChecking.validGamePath():

            gamePath = self.optionsManager.getOption(OPTIONS_GAMEPATH)

            drive = gamePath[0].lower()

            # Starts START_PAYDAY.bat
            # First argument is to change the directory to the game's directory
            # Second argument the drive for the cd command
            # Third argument is the exe name
            subprocess.call([START_PAYDAY_PATH, gamePath, drive, 'payday2_win32_release.exe'])
        else:
            
            logging.error('Could not start PAYDAY 2, could not find payday2_win32_release.exe in:\n%s', gamePath)

            notice = Notice(f'Could not find payday2_win32_release.exe in:\n{gamePath}', 'Error: Invalid Gamepath')
            notice.exec()

    def deselectAllShortcut(self):
        selectedItems = self.modsTable.selectedItems()
        if selectedItems:
            for item in selectedItems:
                item.setSelected(False)
    
    def keyPressEvent(self, event: qtg.QKeyEvent) -> None:
        if event.key() == qt.Key.Key_Delete and self.modsTable.selectedItems():
            self.modsTable.deleteItem()
        return super().keyPressEvent(event)