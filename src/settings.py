import os

import PySide6.QtWidgets as qtw
import PySide6.QtCore as qt

from widgets.progressWidget import ProgressWidget
from threaded.backupMods import BackupMods
from save import OptionsManager, Save
from getPath import Pathing
from style import StyleManager
from widgets.ignoredModsQListWidget import IgnoredMods
from constant_vars import OPTIONS_SECTION, OPTIONS_GAMEPATH, OPTIONS_DISPATH, MODS_DISABLED_PATH_DEFAULT, DARK, LIGHT, OPTIONS_THEME

class Options(qtw.QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.saveManager = Save()
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
        self.gameDir.setText(self.optionsManager.getOption(OPTIONS_GAMEPATH, fallback=''))
        self.gameDir.textChanged.connect(lambda: self.setPath(self.gamePathTimeout.objectName()))

        self.disabledModLabel = qtw.QLabel(self, text='Disabled Mods Path')

        self.disabledModDir = qtw.QLineEdit(self)
        self.disabledModDir.setText(self.optionsManager.getOption(self.disabledModDir.text(), fallback=MODS_DISABLED_PATH_DEFAULT))
        self.disabledModDir.textChanged.connect(lambda: self.setPath(self.disPathTimeout.objectName()))

        gbLayout = qtw.QHBoxLayout()

        self.buttonFrame = qtw.QGroupBox('Color Theme')
    
        self.colorThemeLight = qtw.QPushButton('Light', self.buttonFrame)
        self.colorThemeLight.setCheckable(True)
        self.colorThemeLight.clicked.connect(lambda: self.changeColorTheme(LIGHT))

        self.colorThemeDark = qtw.QPushButton('Dark', self.buttonFrame)
        self.colorThemeDark.setCheckable(True)
        self.colorThemeDark.clicked.connect(lambda: self.changeColorTheme(DARK))

        gbLayout.addWidget(self.colorThemeLight)
        gbLayout.addWidget(self.colorThemeDark)
        
        self.buttonFrame.setLayout(gbLayout)

        # Button group to set exclusive check state to color theme buttons
        self.colorThemeBG = qtw.QButtonGroup(self)
        self.colorThemeBG.setExclusive(True)

        self.colorThemeBG.addButton(self.colorThemeLight, 0)
        self.colorThemeBG.addButton(self.colorThemeDark, 1)

        # Setting color theme buttons' checked state
        if self.optionsManager.getOption(OPTIONS_THEME, LIGHT) == LIGHT:
            self.colorThemeLight.setChecked(True)
        else:
            self.colorThemeDark.setChecked(True)

        # Ignored mods list
        self.ignoredModsListWidget = IgnoredMods(self)
        self.ignoredModsListWidget.itemsChanged.connect(self.updateModIgnoreLabel)

        self.ignoredModsLabel = qtw.QLabel()

        self.backupModsLabel = qtw.QLabel(self, text='This will backup all of your mods and compress it into a zip file.')

        self.backupMods = qtw.QPushButton(parent=self, text='Backup Mods')
        self.backupMods.clicked.connect(lambda: self.startBackupMods())

        self.log = qtw.QPushButton(parent=self, text='Crash Logs')
        self.log.clicked.connect(lambda: os.startfile(os.path.join('C:', 'Users', os.environ['USERNAME'], 'AppData', 'Local', 'PAYDAY 2')))

        self.modLog = qtw.QPushButton(parent=self, text='Mod Crash Logs')
        self.modLog.clicked.connect(lambda: self.openCrashLogBLT())

        for row in ( (self.noticeLabel, self.noticeLabelDesc),
                     (self.gameDirLabel, self.gameDir),
                     (self.disabledModLabel, self.disabledModDir),
                     (self.ignoredModsLabel, self.ignoredModsListWidget),
                     (self.backupModsLabel, self.backupMods),
                     (qtw.QLabel(), self.buttonFrame),
                     (qtw.QLabel(), self.log),
                     (qtw.QLabel(), self.modLog) ):

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
    
    def openCrashLogBLT(self):
        modPath = Pathing().mods()

        os.startfile(os.path.join(modPath, 'logs'))
            
    
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
        self.noticeLabelDesc.setText('Progress has been saved.\n(Remember to move your disabled mods)')
    
    def startBackupMods(self) -> None:
        
        startFileMover = ProgressWidget(BackupMods())
        startFileMover.exec()
    
    def changeColorTheme(self, theme: str):

        self.optionsManager[OPTIONS_SECTION][OPTIONS_THEME] = theme

        app: qtw.QApplication = qtw.QApplication.instance()
        app.setStyleSheet(StyleManager().getStyleSheet(theme))

        self.optionsManager.writeData()
    
    def updateModIgnoreLabel(self) -> None:
        self.ignoredModsLabel.setText(f'Mods Ignored: {self.ignoredModsListWidget.count()}')
