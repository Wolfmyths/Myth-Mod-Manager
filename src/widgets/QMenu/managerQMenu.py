from __future__ import annotations
from typing import TYPE_CHECKING

import PySide6.QtGui as qtg
from PySide6.QtCore import QCoreApplication as qapp

from src.widgets.QMenu.QMenu import ModContextMenu

if TYPE_CHECKING:
    from src.widgets.managerQTableWidget import ModListWidget

class ManagerMenu(ModContextMenu):
    def __init__(self, qParent: ModListWidget) -> None:
        super().__init__(qParent)

        self.qParent = qParent

        self.enable = qtg.QAction(self)
        self.enable.triggered.connect(lambda: self.callFunc(self.qParent.setItemEnabled))

        self.disable = qtg.QAction(self)
        self.disable.triggered.connect(lambda: self.callFunc(self.qParent.setItemDisabled))

        self.delete = qtg.QAction(self)
        self.delete.triggered.connect(lambda: self.callFunc(self.qParent.deleteItem))

        self.checkUpdate = qtg.QAction(self)
        self.checkUpdate.triggered.connect(lambda: self.callFunc(self.qParent.checkModUpdate))

        self.visitModPage = qtg.QAction(self)
        self.visitModPage.triggered.connect(lambda: self.callFunc(self.qParent.visitModPage))

        self.openModDir = qtg.QAction(self)
        self.openModDir.triggered.connect(lambda: self.callFunc(self.qParent.openModDir))

        self.hideMod = qtg.QAction(self)
        self.hideMod.triggered.connect(lambda: self.callFunc(self.qParent.hideMod))

        self.viewTags = qtg.QAction(self)
        self.viewTags.triggered.connect(lambda: self.callFunc(self.qParent.viewTags))

        self.addActions((self.enable, self.disable, self.hideMod, self.delete, self.addSeparator(),
                         self.visitModPage, self.checkUpdate, self.openModDir, self.addSeparator(),
                         self.viewTags))

        self.applyStaticText()

    def applyStaticText(self) -> None:
        self.enable.setText(qapp.translate('ManagerMenu', 'Enable'))
        self.disable.setText(qapp.translate('ManagerMenu', 'Disable'))
        self.delete.setText(qapp.translate('ManagerMenu', 'Delete'))
        self.checkUpdate.setText(qapp.translate('ManagerMenu', 'Check Update'))
        self.visitModPage.setText(qapp.translate('ManagerMenu', 'Visit Page'))
        self.openModDir.setText(qapp.translate('ManagerMenu', 'Open Folder...'))
        self.hideMod.setText(qapp.translate('ManagerMenu', 'Hide'))
        self.viewTags.setText(qapp.translate('ManagerMenu', 'View Tag(s)'))

# EVENT OVERRIDES

    def showEvent(self, event: qtg.QShowEvent) -> None:
        selectedItems = self.qParent.getSelectedNameItems()
        if len(selectedItems) <= 0:
            event.accept()
            return

        if self.qParent.saveManager.getModworkshopAssetID(selectedItems[0].text()):
            self.visitModPage.setEnabled(True)
            self.checkUpdate.setEnabled(True)
        else:
            self.visitModPage.setEnabled(False)
            self.checkUpdate.setEnabled(False)

        return super().showEvent(event)
