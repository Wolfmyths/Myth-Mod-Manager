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

        self.gamePathTimeout = qt.QTimer(self)
        self.gamePathTimeout.setObjectName('gamePathTimeout')
        self.gamePathTimeout.timeout.connect(lambda: self.setGamePathTimeout())

        self.disPathTimeout = qt.QTimer(self)
        self.disPathTimeout.setObjectName('disPathTimeout')
        self.disPathTimeout.timeout.connect(lambda: self.setDisPathTimeout())

        layout = qtw.QFormLayout()
        layout.setContentsMargins(40, 40, 40, 20)
        layout.setRowWrapPolicy(qtw.QFormLayout.RowWrapPolicy.WrapAllRows)

        self.noticeLabel = qtw.QLabel(self)
        self.noticeLabelDesc = qtw.QLabel(self)

        self.gameDirLabel = qtw.QLabel(self, text='Payday 2 Game Path:')

        self.gameDir = qtw.QLineEdit(self)
        self.gameDir.setText(self.optionsManager.get(OPTIONS_SECTION, OPTIONS_GAMEPATH, fallback=''))
        self.gameDir.textChanged.connect(lambda: self.setPath(self.gamePathTimeout.objectName()))

        self.disabledModLabel = qtw.QLabel(self, text='Disabled Mods Path')

        self.disabledModDir = qtw.QLineEdit(self)
        self.disabledModDir.setText(self.optionsManager.get(self.disabledModDir.text(), OPTIONS_DISPATH, fallback=MODS_DISABLED_PATH_DEFAULT))
        self.disabledModDir.textChanged.connect(lambda: self.setPath(self.disPathTimeout.objectName()))

        self.backupModsLabel = qtw.QLabel(self, text='This will backup all of your mods and compress it into a zip file.')

        self.backupMods = qtw.QPushButton(parent=self, text='Backup Mods')
        self.backupMods.clicked.connect(lambda: self.startBackupMods())

        for row in ( (self.noticeLabel, self.noticeLabelDesc),
                     (self.gameDirLabel, self.gameDir),
                     (self.disabledModLabel, self.disabledModDir),
                     (self.backupModsLabel, self.backupMods) ):

            layout.addRow(row[0], row[1])
        
        self.setLayout(layout)
    
    def setPath(self, mode: str):
        '''
        QTimer is started so the save data function isn't called everytime the user changes a single character
        on a QLineEdit
        '''

        timeout: qt.QTimer = self.findChild(qt.QTimer, mode)

        if timeout.objectName() == self.gamePathTimeout.objectName():

            self.noticeLabelDesc.setText('Validating Game Path...')
        
        else:

            self.noticeLabelDesc.setText('Saving disabled games path... do not turn off')

        if not timeout.isActive():

            timeout.start(1000)

        else:

            timeout.stop()
            timeout.start(1000)
            
    
    def setGamePathTimeout(self):

        self.gamePathTimeout.stop()

        gamePath = self.gameDir.text()

        if os.path.exists(os.path.join(gamePath, 'payday2_win32_release.exe')):

            self.noticeLabel.setText('Success:')
            self.noticeLabelDesc.setText('Game Path is valid')

            self.optionsManager[OPTIONS_SECTION][OPTIONS_GAMEPATH] = gamePath

            self.optionsManager.writeData()

        else:

            self.noticeLabel.setText('Error:')
            self.noticeLabelDesc.setText('Game Path is not valid, did not save.')
    
    def setDisPathTimeout(self):

        self.disPathTimeout.stop()

        disPath = self.disabledModDir.text()

        self.optionsManager[OPTIONS_SECTION][OPTIONS_DISPATH] = disPath

        self.optionsManager.writeData()

        self.noticeLabel.setText('Success:')
        self.noticeLabelDesc.setText('Progress has been saved')
    
    def startBackupMods(self) -> None:
        
        outcome = FileMover().backupMods()

        if outcome == 1:

            self.noticeLabel.setText('Success:')
            self.noticeLabelDesc.setText("Your backup has been saved to the manager's directory")

        else:

            self.noticeLabel.setText('Error:')
            self.noticeLabelDesc.setText('Something went wrong, changes have been reverted.')
