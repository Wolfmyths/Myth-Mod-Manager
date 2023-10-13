from __future__ import annotations
from typing import TYPE_CHECKING

import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg

import src.errorChecking as errorChecking

from src.widgets.QDialog.announcementQDialog import Notice
from src.widgets.progressWidget import ProgressWidget
from src.widgets.modProfileQTreeWidget import ProfileList
from src.threaded.moveToDisabledDir import MoveToDisabledDir
from src.threaded.moveToEnabledDir import MoveToEnabledModDir
from src.save import OptionsManager, Save

if TYPE_CHECKING:
    from src.widgets.managerQTableWidget import ModListWidget

class modProfile(qtw.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.saveManager = Save()

        self.optionsManager = OptionsManager()

        layout = qtw.QVBoxLayout()

        self.profileDisplay = ProfileList(self)

        self.profileDisplay.applyProfile.connect(lambda x: self.applyMods(x))

        self.deselectAllShortcut = qtg.QShortcut(qtg.QKeySequence("Ctrl+D"), self)
        self.deselectAllShortcut.activated.connect(lambda: self.profileDisplay.unselectShortcut())

        for widget in (self.profileDisplay, ):
            layout.addWidget(widget)
        
        self.setLayout(layout)

    def applyMods(self, mods: list[str]):

        enableMods = ProgressWidget(MoveToEnabledModDir(*[x for x in mods if errorChecking.isInstalled(x)]))
        enableMods.exec()

        disableMods = ProgressWidget(MoveToDisabledDir(*[x for x in self.saveManager.sections() if errorChecking.isInstalled(x) and x not in mods]))
        disableMods.exec()

        # Refresh table so it is updated after all of this is done
        widget: ModListWidget
        for widget in qtw.QApplication.allWidgets():
            if str(widget.__class__) == "<class 'widgets.managerQTableWidget.ModListWidget'>":
                widget.refreshMods()
                break

        notInstalledMods = [x for x in mods if not errorChecking.isInstalled(x)]

        if notInstalledMods:
            notice = Notice(f'The following mods were not applied because they are not installed:\n{" ,".join(notInstalledMods)}', 'Info: Some mods were not applied')
            notice.exec()
