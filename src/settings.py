import os

import PySide6.QtWidgets as qtw
import PySide6.QtCore as qt

from fileMover import FileMover
from save import OptionsManager
from constant_vars import OPTIONS_SECTION, OPTIONS_GAMEPATH, OPTIONS_DISPATH, MODS_DISABLED_PATH_DEFAULT

class Options(qtw.QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.optionsManager = OptionsManager()

        self.timeout = qt.QTimer()
        self.timeout.timeout.connect(lambda: self.setGamePathTimeout())

        layout = qtw.QFormLayout()
        layout.setContentsMargins(40, 40, 40, 20)
        layout.setRowWrapPolicy(qtw.QFormLayout.RowWrapPolicy.WrapAllRows)

        self.noticeLabel = qtw.QLabel(self)
        self.noticeLabelDesc = qtw.QLabel(self)

        self.gameDirLabel = qtw.QLabel(self, text='Payday 2 Game Path:')

        self.gameDir = qtw.QLineEdit(self)
        self.gameDir.setText(self.optionsManager.get(OPTIONS_SECTION, OPTIONS_GAMEPATH, fallback=''))
        self.gameDir.textChanged.connect(lambda: self.setGamePath())

        self.disabledModLabel = qtw.QLabel(self, text='Disabled Mods Path')

        self.disabledModDir = qtw.QLineEdit(self)
        self.disabledModDir.setText(self.optionsManager.get(self.disabledModDir.text(), OPTIONS_DISPATH, fallback=MODS_DISABLED_PATH_DEFAULT))
        self.disabledModDir.textChanged.connect(lambda: self.optionsManager.setOption(self.disabledModDir.text(), OPTIONS_DISPATH))

        self.backupModsLabel = qtw.QLabel(self, text='This will backup all of your mods and compress it into a zip file.')

        self.backupMods = qtw.QPushButton(parent=self, text='Backup Mods')
        self.backupMods.clicked.connect(lambda: self.startBackupMods())

        for row in ( (self.noticeLabel, self.noticeLabelDesc),
                     (self.gameDirLabel, self.gameDir),
                     (self.disabledModLabel, self.disabledModDir),
                     (self.backupModsLabel, self.backupMods) ):

            layout.addRow(row[0], row[1])
        
        self.setLayout(layout)
    
    def setGamePath(self):
        '''
        QTimer is started so the save data function isn't called everytime the user changes a single character

        setGamePathTimeout() is the function that actually saves the gamePath
        '''

        self.noticeLabelDesc.setText('Validating Game Path...')

        if not self.timeout.isActive():

            self.timeout.start(1000)

        else:

            self.timeout.stop()
            self.timeout.start(1000)
            
    
    def setGamePathTimeout(self):

        self.timeout.stop()

        gamePath = self.gameDir.text()

        if os.path.exists(os.path.join(gamePath, 'payday2_win32_release.exe')):

            self.noticeLabel.setText('Success:')
            self.noticeLabelDesc.setText('Game Path is valid')

            self.optionsManager[OPTIONS_SECTION][OPTIONS_GAMEPATH] = gamePath

            self.optionsManager.writeData()

        else:

            self.noticeLabel.setText('Error:')
            self.noticeLabelDesc.setText('Game Path is not valid')
    
    def startBackupMods(self) -> None:
        
        outcome = FileMover().backupMods()

        if outcome == 1:

            text = "Mods backed up at MMM's directory"

        else:

            text = 'Error: Mods could not be backed up'

        self.backupModsLabel.setText(text)
