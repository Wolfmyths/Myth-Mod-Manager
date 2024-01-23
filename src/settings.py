import os
import logging
import sys

import PySide6.QtWidgets as qtw
from PySide6.QtCore import QCoreApplication

from src.widgets.progressWidget import ProgressWidget
from src.threaded.backupMods import BackupMods
from src.save import OptionsManager
from src.getPath import Pathing
from src.style import StyleManager
from src.widgets.ignoredModsQListWidget import IgnoredMods
from src.constant_vars import DARK, LIGHT, OPTIONS_CONFIG, ROOT_PATH
from src.widgets.QDialog.newUpdateQDialog import updateDetected
from src.widgets.QDialog.announcementQDialog import Notice

from src.api.checkUpdate import checkUpdate

from src import errorChecking

class Options(qtw.QWidget):

    def __init__(self, optionsPath = OPTIONS_CONFIG) -> None:
        super().__init__()

        logging.getLogger(__file__)

        layout = qtw.QFormLayout()
        layout.setContentsMargins(40, 40, 40, 20)
        layout.setVerticalSpacing(10)
        layout.setRowWrapPolicy(qtw.QFormLayout.RowWrapPolicy.WrapAllRows)

        self.optionsManager = OptionsManager(optionsPath)

        self.updateAlertCheckbox = qtw.QCheckBox(self, text='Update alerts on startup')
        self.updateAlertCheckbox.setChecked(self.optionsManager.getMMMUpdateAlert())
        self.updateAlertCheckbox.clicked.connect(self.setUpdateAlert)

        self.checkUpdateButton = qtw.QPushButton(self, text='Check for updates')
        self.checkUpdateButton.clicked.connect(self.checkUpdate)

        self.gameDirLabel = qtw.QLabel(self, text='Payday 2 Game Path:')

        self.gameDir = qtw.QLineEdit(self)
        self.gameDir.setText(self.optionsManager.getGamepath())
        self.gameDir.textChanged.connect(lambda x: self.setGamePath(x))

        self.disabledModLabel = qtw.QLabel(self, text='Disabled Mods Path')

        self.disabledModDir = qtw.QLineEdit(self)
        self.disabledModDir.setText(self.optionsManager.getDispath())
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
        if self.optionsManager.getTheme() == LIGHT:
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

        for row in ( (self.updateAlertCheckbox, self.checkUpdateButton),
                     (self.gameDirLabel, self.gameDir),
                     (self.disabledModLabel, self.disabledModDir),
                     (self.ignoredModsLabel, self.ignoredModsListWidget),
                     (self.backupModsLabel, self.backupMods),
                     (qtw.QLabel(), self.buttonFrame),
                     (qtw.QLabel(), self.log),
                     (qtw.QLabel(), self.modLog) ):

            layout.addRow(row[0], row[1])

        self.setLayout(layout)
    
    def setUpdateAlert(self) -> None:
        alert = self.updateAlertCheckbox.isChecked()
        self.optionsManager.setMMMUpdateAlert(alert)
        self.optionsManager.writeData()
    
    def checkUpdate(self) -> None:
        def updateFound(latestVersion: str, changelog: str) -> None:
            notice = updateDetected(latestVersion, changelog)
            notice.rejected.connect(lambda: self.checkUpdateButton.setText('Check for updates'))
            notice.exec()
            
            if notice.result():
                os.startfile(os.path.join(ROOT_PATH, 'Myth Mod Manager.exe'))
                QCoreApplication.quit()

        self.checkUpdateButton.setText('Checking...')

        self.run_checkupdate = checkUpdate()
        self.run_checkupdate.updateDetected.connect(lambda x, y: updateFound(x, y))
        self.run_checkupdate.error.connect(lambda: self.checkUpdateButton.setText('Error: Check logs for more info'))
        self.run_checkupdate.upToDate.connect(lambda: self.checkUpdateButton.setText('Up to date! ^_^'))

    def openCrashLogBLT(self) -> None:
        modPath = Pathing().mods()

        errorChecking.startFile(os.path.join(modPath, 'logs'))
    
    def openCrashLogs(self) -> None:

        if sys.platform.startswith('win'):
            os.startfile(os.path.join('C:', 'Users', os.environ['USERNAME'], 'AppData', 'Local', 'PAYDAY 2'))
        else:
            notice = Notice(
                'Overkill did not implement a vanilla crash log for linux :(',
                'Myth Mod Manager: Vanilla crashlogs unsupported'
                )
            notice.exec()
            
    
    def setGamePath(self, path: str) -> None:

        if os.path.isfile(os.path.join(path, 'payday2_win32_release.exe')):

            logging.info('Changed game path to: %s', path)

            self.optionsManager.setGamepath(path)
            self.optionsManager.writeData()
    
    def setDisPath(self, path: str) -> None:

        logging.info('Changed disabled mod folder path to: %s', path)

        self.optionsManager.setDispath(path)
        self.optionsManager.writeData()
    
    def startBackupMods(self) -> None:
        
        startFileMover = ProgressWidget(BackupMods())
        startFileMover.exec()
    
    def changeColorTheme(self, theme: str) -> None:

        self.optionsManager.setTheme(theme)

        app: qtw.QApplication = qtw.QApplication.instance()
        app.setStyleSheet(StyleManager().getStyleSheet(theme))
    
    def updateModIgnoreLabel(self) -> None:
        self.ignoredModsLabel.setText(f'Hidden Mods: {self.ignoredModsListWidget.count()}')
