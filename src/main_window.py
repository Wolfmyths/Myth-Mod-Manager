import os

import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw
from PySide6.QtCore import QCoreApplication as qapp, QEvent, Slot

from src.manager import ModManager
from src.tools import ToolManager
from src.settings import Options
from src.profiles import modProfile
from src.widgets.aboutQWidget import About
from src.widgets.QDialog.newUpdateQDialog import updateDetected
from src.save import OptionsManager
from src.api.checkUpdate import checkUpdate

from src.constant_vars import ICON, PROGRAM_NAME, VERSION, ROOT_PATH
from src import errorChecking

class MainWindow(qtw.QMainWindow):
    def __init__(self, app: qapp | None = None) -> None:
        super().__init__()

        self.setWindowIcon(qtg.QIcon(ICON))
        self.setWindowTitle(f'{PROGRAM_NAME} {VERSION}')
        self.setMinimumSize(800, 800)
        self.resize(OptionsManager.getWindowSize())

        self.app: qapp | None = app

        self.tab = qtw.QTabWidget(self)

        self.manager = ModManager()
        self.profile = modProfile()
        self.tools = ToolManager()
        self.options = Options()
        self.about = About()

        self.options.ignoredMods.ignoredModsListWidget.itemsRemoved.connect(self.manager.modsTable.refreshMods)
        self.options.themeSwitched.connect(self.manager.modsTable.swapIcons)
        self.options.themeSwitched.connect(self.about.updateIcons)

        for page in (
                        (self.manager, ''),
                        (self.profile, ''),
                        (self.tools, ''),
                        (self.options, ''),
                        (self.about, '')
                    ):

            self.tab.addTab(page[0], page[1])

        self.setCentralWidget(self.tab)

        self.applyStaticText()

        if OptionsManager.getMMMUpdateAlert():
            self.run_checkUpdate = checkUpdate()
            self.run_checkUpdate.updateDetected.connect(self.updateDetected)

    def applyStaticText(self) -> None:
        tab: qtw.QTabBar = self.tab.tabBar()
        tab.setTabText(0, qapp.translate('MainWindow', 'Manager'))
        tab.setTabText(1, qapp.translate('MainWindow', 'Profiles'))
        tab.setTabText(2, qapp.translate('MainWindow', 'Tools'))
        tab.setTabText(3, qapp.translate('MainWindow', 'Options'))
        tab.setTabText(4, qapp.translate('MainWindow', 'About'))

    @Slot(str, str)
    def updateDetected(self, latestVersion: str, changelog: str) -> None:
        notice = updateDetected(latestVersion, changelog)
        notice.exec()

        if notice.result():
            errorChecking.startFile(os.path.join(ROOT_PATH, 'Myth Mod Manager.exe'))
            qapp.quit()

    @Slot()
    def languageChange(self) -> None:
        self.applyStaticText()

        self.manager.applyStaticText()
        self.manager.updateModCount()

        self.manager.modsTable.applyStaticText()
        self.manager.modsTable.contextMenu.applyStaticText()

        if self.manager.modsTable.tagViewer is not None:
            self.manager.modsTable.tagViewer.applyStaticText()
            self.manager.modsTable.tagViewer.tagQTable.applyStaticText()
            self.manager.modsTable.tagViewer.contextMenu.applyStaticText()

        self.profile.profileDisplay.applyStaticText()
        self.profile.profileDisplay.menu.applyStaticText()

        self.about.applyStaticText()

        self.tools.applyStaticText()
        for items in self.tools.toolsWidget.external_tools:
            items.applyStaticText()

        self.options.applyStaticText()
        self.options.ignoredMods.ignoredModsListWidget.contextMenu.applyStaticText()
        self.options.optionsGeneral.applyStaticText()
        self.options.shortcuts.applyStaticText()
        self.options.optionsMisc.applyStaticText()

    def closeEvent(self, event: qtg.QCloseEvent) -> None:
        OptionsManager.setWindowSize(self.size())
        OptionsManager.writeData()

        if isinstance(self.app, qtw.QApplication):
            self.app.closeAllWindows()
        return super().closeEvent(event)

    def event(self, event: QEvent) -> None:
        if event.type() == QEvent.Type.LanguageChange:
            self.languageChange()
 
        return super().event(event)
