from __future__ import annotations

import logging

import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
from PySide6.QtCore import QCoreApplication as qapp, Slot

import src.helpers.helper as helper

from src.widgets.qdialog.notice import Notice
from src.widgets.qdialog.progress_widget import ProgressWidget
from src.widgets.qtreewidget.profile_list import ProfileList
from src.widgets.qtable.mod_list_widget import ModListWidget
from src.objects.move_to_disabled_dir import MoveToDisabledDir
from src.objects.move_to_enabled_dir import MoveToEnabledModDir
from src.helpers.save_manager import Save

class ModProfile(qtw.QWidget):
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
        disabledMods: list[str] = [x for x in mods if helper.isInstalled(x)]
        enabledMods: list[str] = [x for x in Save.mods() if helper.isInstalled(x) and x not in mods]
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
        for widget in qtw.QApplication.allWidgets():
            if isinstance(widget, ModListWidget):
                widget.refreshMods()
                break

        notInstalledMods: list[str] = [x for x in mods if not helper.isInstalled(x)]

        if notInstalledMods:
            notice = Notice(
                qapp.translate("modProfile", 'The following mods were not applied because they are not installed:') + 
                f'\n{" ,".join(notInstalledMods)}',
                qapp.translate("modProfile", 'Profile: Some mods were not applied')
            )
            notice.exec()
