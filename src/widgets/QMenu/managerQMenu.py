from __future__ import annotations
from typing import TYPE_CHECKING

import PySide6.QtGui as qtg

from src.widgets.QMenu.QMenu import ModContextMenu

if TYPE_CHECKING:
    from src.widgets.managerQTableWidget import ModListWidget

class ManagerMenu(ModContextMenu):
    def __init__(self, qParent: ModListWidget) -> None:
        super().__init__(qParent)

        self.qParent = qParent

        self.enable = qtg.QAction('Enable', self)
        self.enable.triggered.connect(lambda: self.callFunc(self.qParent.setItemEnabled))

        self.disable = qtg.QAction('Disable', self)
        self.disable.triggered.connect(lambda: self.callFunc(self.qParent.setItemDisabled))

        self.delete = qtg.QAction('Delete', self)
        self.delete.triggered.connect(lambda: self.callFunc(self.qParent.deleteItem))

        self.checkUpdate = qtg.QAction('Check Update', self)
        self.checkUpdate.triggered.connect(lambda: self.callFunc(self.qParent.checkModUpdate))

        self.visitModPage = qtg.QAction('Visit Page', self)
        self.visitModPage.triggered.connect(lambda: self.callFunc(self.qParent.visitModPage))

        self.openModDir = qtg.QAction('Open Dir...', self)
        self.openModDir.triggered.connect(lambda: self.callFunc(self.qParent.openModDir))

        self.hideMod = qtg.QAction('Hide', self)
        self.hideMod.triggered.connect(lambda: self.callFunc(self.qParent.hideMod))

        self.viewTags = qtg.QAction('View Tag(s)', self)
        self.viewTags.triggered.connect(lambda: self.callFunc(self.qParent.viewTags))

        self.addActions((self.enable, self.disable, self.hideMod, self.delete, self.addSeparator(),
                         self.visitModPage, self.checkUpdate, self.openModDir, self.addSeparator(),
                         self.viewTags))

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
