import os
import logging

import PySide6.QtWidgets as qtw

from src.widgets.progressWidget import ProgressWidget
from src.threaded.backupMods import BackupMods
from src.save import OptionsManager
from src.getPath import Pathing
from src.style import StyleManager
from src.widgets.ignoredModsQListWidget import IgnoredMods
from src.constant_vars import OPTIONS_SECTION, OPTIONS_GAMEPATH, OPTIONS_DISPATH, MODS_DISABLED_PATH_DEFAULT, DARK, LIGHT, OPTIONS_THEME

class Options(qtw.QWidget):

    def __init__(self) -> None:
        super().__init__()

        logging.getLogger(__file__)

        layout = qtw.QFormLayout()
        layout.setContentsMargins(40, 40, 40, 20)
        layout.setVerticalSpacing(10)
        layout.setRowWrapPolicy(qtw.QFormLayout.RowWrapPolicy.WrapAllRows)

        self.optionsManager = OptionsManager()

        self.gameDirLabel = qtw.QLabel(self, text='Payday 2 Game Path:')

        self.gameDir = qtw.QLineEdit(self)
        self.gameDir.setText(self.optionsManager.getOption(OPTIONS_GAMEPATH, fallback=''))
        self.gameDir.textChanged.connect(lambda x: self.setGamePath(x))

        self.disabledModLabel = qtw.QLabel(self, text='Disabled Mods Path')

        self.disabledModDir = qtw.QLineEdit(self)
        self.disabledModDir.setText(self.optionsManager.getOption(OPTIONS_DISPATH, fallback=MODS_DISABLED_PATH_DEFAULT))
        self.disabledModDir.textChanged.connect(lambda x: self.setDisPath(x))

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
        self.backupMods.clicked.connect(self.startBackupMods)

        self.log = qtw.QPushButton(parent=self, text='Crash Logs')
        self.log.clicked.connect(self.openCrashLogs)

        self.modLog = qtw.QPushButton(parent=self, text='Mod Crash Logs')
        self.modLog.clicked.connect(lambda: self.openCrashLogBLT())

        for row in ( (self.gameDirLabel, self.gameDir),
                     (self.disabledModLabel, self.disabledModDir),
                     (self.ignoredModsLabel, self.ignoredModsListWidget),
                     (self.backupModsLabel, self.backupMods),
                     (qtw.QLabel(), self.buttonFrame),
                     (qtw.QLabel(), self.log),
                     (qtw.QLabel(), self.modLog) ):

            layout.addRow(row[0], row[1])

        self.setLayout(layout)

    def openCrashLogBLT(self) -> None:
        modPath = Pathing().mods()

        os.startfile(os.path.join(modPath, 'logs'))
    
    def openCrashLogs(self) -> None:
        os.startfile(os.path.join('C:', 'Users', os.environ['USERNAME'], 'AppData', 'Local', 'PAYDAY 2'))            
    
    def setGamePath(self, path: str) -> None:

        if os.path.exists(os.path.join(path, 'payday2_win32_release.exe')):

            logging.info('Changed game path to: %s', path)

            self.optionsManager[OPTIONS_SECTION][OPTIONS_GAMEPATH] = path

            self.optionsManager.writeData()
    
    def setDisPath(self, path: str) -> None:

        logging.info('Changed disabled mod folder path to: %s', path)

        self.optionsManager[OPTIONS_SECTION][OPTIONS_DISPATH] = path

        self.optionsManager.writeData()
    
    def startBackupMods(self) -> None:
        
        startFileMover = ProgressWidget(BackupMods())
        startFileMover.exec()
    
    def changeColorTheme(self, theme: str):

        self.optionsManager[OPTIONS_SECTION][OPTIONS_THEME] = theme

        app: qtw.QApplication = qtw.QApplication.instance()
        app.setStyleSheet(StyleManager().getStyleSheet(theme))

        self.optionsManager.writeData()
    
    def updateModIgnoreLabel(self) -> None:
        self.ignoredModsLabel.setText(f'Hidden Mods: {self.ignoredModsListWidget.count()}')
