import os
import subprocess
import logging
import sys

import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt as qt
import PySide6.QtGui as qtg

from src.widgets.managerQTableWidget import ModListWidget
from src.widgets.QDialog.announcementQDialog import Notice
from src.save import Save, OptionsManager
import src.errorChecking as errorChecking
from src.constant_vars import ModType, MOD_CONFIG, OPTIONS_CONFIG

class ModManager(qtw.QWidget):

    def __init__(self, saveManagerPath = MOD_CONFIG, optionsManagerPath = OPTIONS_CONFIG) -> None:
        super().__init__()

        self.setObjectName('manager')
        self.selectAllShortCut = qtg.QShortcut(qtg.QKeySequence("Ctrl+A"), self)
        self.selectAllShortCut.activated.connect(lambda: self.modsTable.selectAll())

        self.deselectAllShortCut = qtg.QShortcut(qtg.QKeySequence("Ctrl+D"), self)
        self.deselectAllShortCut.activated.connect(self.deselectAllShortcut)

        self.saveManager = Save(saveManagerPath)
        self.optionsManager = OptionsManager(optionsManagerPath)

        layout = qtw.QVBoxLayout()

        self.setAcceptDrops(True)

        self.refresh = qtw.QPushButton('Refresh Mods', self)
        self.refresh.clicked.connect(lambda: self.modsTable.refreshMods())

        self.openGameDir = qtw.QPushButton('Open Game Directory', self)
        self.openGameDir.clicked.connect(lambda: errorChecking.startFile(self.optionsManager.getGamepath()))

        self.startGame = qtw.QPushButton('Start PAYDAY 2', self)
        self.startGame.clicked.connect(self.startPayday)

        modLabelLayout = qtw.QHBoxLayout()
        modLabelLayout.setSpacing(100)
        modLabelLayout.setAlignment(qt.AlignmentFlag.AlignHCenter)

        self.labelFrame = qtw.QFrame()

        self.totalModsLabel = qtw.QLabel('Total Mods: 0', self)

        self.modsLabel = qtw.QLabel('Mods: 0', self)

        self.overrideLabel = qtw.QLabel('Mod_Overrides: 0', self)

        self.mapsLabel = qtw.QLabel('Maps: 0', self)

        for widget in (self.totalModsLabel, self.modsLabel, self.overrideLabel, self.mapsLabel):
            modLabelLayout.addWidget(widget)

        self.labelFrame.setLayout(modLabelLayout)

        self.search = qtw.QLineEdit()
        self.search.setPlaceholderText('Search... use "tag:" with no spaces to search for tags, use a comma "," to seperate tags')
        self.search.textChanged.connect(lambda x: self.modsTable.search(x))

        self.modsTable = ModListWidget(saveManagerPath, optionsManagerPath)
        self.modsTable.itemChanged.connect(self.updateModCount)

        self.modsTable.refreshMods()

        for widget in (self.refresh, self.openGameDir, self.startGame, self.labelFrame, self.search, self.modsTable):
            layout.addWidget(widget)

        self.setLayout(layout)
    
    def updateModCount(self):

        self.totalModsLabel.setText(f'Total Mods: {self.modsTable.rowCount()}')

        self.modsLabel.setText(f'Mods: {self.modsTable.getModTypeCount(ModType.mods)}')

        self.overrideLabel.setText(f'Mod_Overrides: {self.modsTable.getModTypeCount(ModType.mods_override)}')

        self.mapsLabel.setText(f'Maps: {self.modsTable.getModTypeCount(ModType.maps)}')

    def startPayday(self):

        gamePath: str = self.optionsManager.getGamepath()

        try:
            if not os.path.isabs(gamePath):
                raise Exception('Path is not absolute')

            if sys.platform.startswith('win'):

                gameExe = 'payday2_win32_release.exe'

                # TODO: Permission error is raised without shell=True, can this be avoided?
                cmd = subprocess.run([gamePath[0:2].upper(), '&&', 'cd', gamePath, '&&', gameExe], shell=True)
                cmd.check_returncode()
            else:
                gameExe = 'payday2_release'
                errorChecking.startFile(os.path.join(gamePath, gameExe))

        except Exception as e:
            logging.error('An error occured trying to start PAYDAY 2:\n%s', str(e))
            notice = Notice(f'An error occured trying to start PAYDAY 2:\n{e}', 'Could not start PAYDAY 2 from MMM')
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
