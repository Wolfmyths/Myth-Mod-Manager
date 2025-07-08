from __future__ import annotations

import logging

import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
from PySide6.QtCore import QCoreApplication as qapp, Slot

import src.errorChecking as errorChecking

from src.widgets.QDialog.announcementQDialog import Notice
from src.widgets.progressWidget import ProgressWidget
from src.widgets.modProfileQTreeWidget import ProfileList
from src.widgets.managerQTableWidget import ModListWidget
from src.threaded.moveToDisabledDir import MoveToDisabledDir
from src.threaded.moveToEnabledDir import MoveToEnabledModDir
from src.save import Save

class modProfile(qtw.QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = qtw.QVBoxLayout()

        self.addProfileButton = qtw.QPushButton(self)

        self.profileDisplay = ProfileList(self)

        self.addProfileButton.clicked.connect(self.profileDisplay.menuAddProfile)
        self.profileDisplay.applyProfile.connect(self.applyMods)

        self.deselectAllShortcut = qtg.QShortcut(qtg.QKeySequence("Ctrl+D"), self)
        self.deselectAllShortcut.activated.connect(self.profileDisplay.unselectShortcut)

        for widget in (self.addProfileButton, self.profileDisplay):
            layout.addWidget(widget)
        
        self.setLayout(layout)
        self.applyStaticText()

    def applyStaticText(self) -> None:
        self.addProfileButton.setText(qapp.translate('modProfile', 'Add Profile'))

    @Slot(tuple)
    def applyMods(self, mods: tuple[str, ...]) -> None:
        disabledMods: list[str] = [x for x in mods if errorChecking.isInstalled(x)]
        enabledMods: list[str] = [x for x in Save.mods() if errorChecking.isInstalled(x) and x not in mods]
        enableProgressWidget = ProgressWidget(MoveToEnabledModDir(*disabledMods))
        disableProgressWidget = ProgressWidget(MoveToDisabledDir(*enabledMods))

        notice = Notice('Canceled or something went wrong when applying the mod profile')

        logging.info('Enabled mods to be disabled:%s\nDisabled mods to be disabled:%s', enabledMods, disabledMods)
        if enableProgressWidget.exec() != qtw.QDialog.DialogCode.Accepted:
            notice.exec()
            return

        if disableProgressWidget.exec() != qtw.QDialog.DialogCode.Accepted:
            notice.exec()
            return

        # Refresh table so it is updated after all of this is done
        # TODO: Refactor to make this not loop through all widgets
        widget: ModListWidget
        for widget in qtw.QApplication.allWidgets():
            if isinstance(widget, ModListWidget):
                widget.refreshMods()
                break

        notInstalledMods: list[str] = [x for x in mods if not errorChecking.isInstalled(x)]

        if notInstalledMods:
            notice = Notice(
                qapp.translate("modProfile", 'The following mods were not applied because they are not installed:') + 
                f'\n{" ,".join(notInstalledMods)}',
                qapp.translate("modProfile", 'Profile: Some mods were not applied')
            )
            notice.exec()
