from __future__ import annotations
from typing import TYPE_CHECKING

from typing_extensions import override

import PySide6.QtGui as qtg
from PySide6.QtCore import QCoreApplication as qapp

from src.widgets.qmenu.mod_context_menu import ModContextMenu

if TYPE_CHECKING:
    import PySide6.QtWidgets as qtw

class ManagerMenu(ModContextMenu):
    def __init__(self, qParent: qtw.QWidget | None = None) -> None:
        super().__init__(qParent)

        self.enable = qtg.QAction(self)

        self.disable = qtg.QAction(self)
        self.delete = qtg.QAction(self)

        self.checkUpdate = qtg.QAction(self)

        self.visitModPage = qtg.QAction(self)

        self.openModDir = qtg.QAction(self)

        self.hideMod = qtg.QAction(self)

        self.viewTags = qtg.QAction(self)

        self.addActions((self.enable, self.disable, self.hideMod, self.delete, self.addSeparator(),
                         self.visitModPage, self.checkUpdate, self.openModDir, self.addSeparator(),
                         self.viewTags))

        self.applyStaticText()

    @override
    def applyStaticText(self) -> None:
        self.enable.setText(qapp.translate('ManagerMenu', 'Enable'))
        self.disable.setText(qapp.translate('ManagerMenu', 'Disable'))
        self.delete.setText(qapp.translate('ManagerMenu', 'Delete'))
        self.checkUpdate.setText(qapp.translate('ManagerMenu', 'Check Update'))
        self.visitModPage.setText(qapp.translate('ManagerMenu', 'Visit Page'))
        self.openModDir.setText(qapp.translate('ManagerMenu', 'Open Folder...'))
        self.hideMod.setText(qapp.translate('ManagerMenu', 'Hide'))
        self.viewTags.setText(qapp.translate('ManagerMenu', 'View Tag(s)'))
