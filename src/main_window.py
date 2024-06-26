import os

import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw
from PySide6.QtCore import QCoreApplication

from src.manager import ModManager
from src.tools import ToolManager
from src.settings import Options
from src.profiles import modProfile
from src.widgets.aboutQWidget import About
from src.widgets.QDialog.newUpdateQDialog import updateDetected
from src.save import OptionsManager, Save
from src.api.checkUpdate import checkUpdate

from src.constant_vars import ICON, PROGRAM_NAME, VERSION, MOD_CONFIG, OPTIONS_CONFIG, ROOT_PATH
from src import errorChecking

class MainWindow(qtw.QMainWindow):
    def __init__(self, app: qtw.QApplication | None = None, savePath = MOD_CONFIG, optionsPath = OPTIONS_CONFIG) -> None:
        super().__init__()

        self.optionsManager = OptionsManager(optionsPath)
        self.save = Save(savePath)

        self.setWindowIcon(qtg.QIcon(ICON))
        self.setWindowTitle(f'{PROGRAM_NAME} {VERSION}')
        self.setMinimumSize(800, 800)
        self.resize(self.optionsManager.getWindowSize())

        self.app = app

        self.tab = qtw.QTabWidget(self)

        self.manager = ModManager(savePath, optionsPath)
        self.profile = modProfile()
        self.tools = ToolManager()
        self.options = Options()
        self.about = About()

        self.options.ignoredMods.ignoredModsListWidget.itemsRemoved.connect(self.manager.modsTable.refreshMods)
        self.options.themeSwitched.connect(lambda x: self.manager.modsTable.swapIcons(x))
        self.options.themeSwitched.connect(lambda x: self.about.updateIcons(x))

        for page in (
                        (self.manager, 'Manager'),
                        (self.profile, 'Profiles'),
                        (self.tools, 'Tools'),
                        (self.options, 'Options'),
                        (self.about, 'About')
                    ):

            self.tab.addTab(page[0], page[1])

        self.setCentralWidget(self.tab)

        if self.optionsManager.getMMMUpdateAlert():
            self.run_checkUpdate = checkUpdate()
            self.run_checkUpdate.updateDetected.connect(lambda x, y: self.updateDetected(x, y))
    
    def updateDetected(self, latestVersion: str, changelog: str) -> None:
        notice = updateDetected(latestVersion, changelog)
        notice.exec()
        
        if notice.result():
            errorChecking.startFile(os.path.join(ROOT_PATH, 'Myth Mod Manager.exe'))
            QCoreApplication.quit()
    
    def closeEvent(self, event: qtg.QCloseEvent) -> None:
        self.optionsManager.setWindowSize(self.size())
        self.optionsManager.writeData()

        if isinstance(self.app, qtw.QApplication):
            self.app.closeAllWindows()
        return super().closeEvent(event)
