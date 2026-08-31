import os

import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw
from PySide6.QtCore import QCoreApplication as qapp, QEvent, Slot
from typing_extensions import override

from src.widgets.qwidget.mod_manager import ModManager
from src.widgets.qwidget.tool_manager import ToolManager
from src.widgets.qwidget.options import Options
from src.widgets.qwidget.mod_profile import ModProfile
from src.widgets.qwidget.about import About
from src.widgets.qdialog.update_detected import UpdateDetected
from src.helpers.options_manager import OptionsManager
from src.api.check_update import CheckUpdate

from src.constant_vars import ICON, PROGRAM_NAME, VERSION, ROOT_PATH
from src.helpers import helper

class MainWindow(qtw.QMainWindow):
    def __init__(self, app: qapp | None = None) -> None:
        super().__init__()

        self.setWindowIcon(qtg.QIcon(ICON))
        self.setWindowTitle(f'{PROGRAM_NAME} {VERSION.toString()}')
        self.setMinimumSize(800, 600)
        self.resize(OptionsManager.getWindowSize())

        self.app: qapp | None = app

        self.tab = qtw.QTabWidget(self)

        self.manager = ModManager()
        self.profile = ModProfile()
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
            self.run_CheckUpdate = CheckUpdate()
            self.run_CheckUpdate.updateDetected.connect(self.updateDetected)

    def applyStaticText(self) -> None:
        tab: qtw.QTabBar = self.tab.tabBar()
        tab.setTabText(0, qapp.translate('MainWindow', 'Manager'))
        tab.setTabText(1, qapp.translate('MainWindow', 'Profiles'))
        tab.setTabText(2, qapp.translate('MainWindow', 'Tools'))
        tab.setTabText(3, qapp.translate('MainWindow', 'Options'))
        tab.setTabText(4, qapp.translate('MainWindow', 'About'))

    @Slot(str, str)
    def updateDetected(self, latestVersion: str, changelog: str) -> None:
        notice = UpdateDetected(latestVersion, changelog)
        notice.exec()

        if notice.result():
            helper.startFile(os.path.join(ROOT_PATH, 'Myth Mod Manager.exe'))
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

    @override
    def closeEvent(self, event: qtg.QCloseEvent) -> None:
        OptionsManager.setWindowSize(self.size())
        OptionsManager.writeData()

        if isinstance(self.app, qtw.QApplication):
            self.app.closeAllWindows()
        return super().closeEvent(event)

    @override
    def event(self, event: QEvent) -> bool:
        if event.type() == QEvent.Type.LanguageChange:
            self.languageChange()
 
        return super().event(event)
