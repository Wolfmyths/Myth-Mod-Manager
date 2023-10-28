from __future__ import annotations
from typing import TYPE_CHECKING

import PySide6.QtGui as qtg

from src.widgets.QMenu.QMenu import ModContextMenu

from src.save import Save

if TYPE_CHECKING:
    from src.widgets.managerQTableWidget import ModListWidget

class ManagerMenu(ModContextMenu):
    def __init__(self, qParent: ModListWidget) -> None:
        super().__init__(qParent)

        self.qParent = qParent

        self.enable = qtg.QAction('Enable', self)
        self.enable.triggered.connect(self.enabledClicked)

        self.disable = qtg.QAction('Disable', self)
        self.disable.triggered.connect(self.disabledClicked)

        self.delete = qtg.QAction('Delete', self)
        self.delete.triggered.connect(self.deleteClicked)

        self.visitModPage = qtg.QAction('Visit Page', self)
        self.visitModPage.triggered.connect(self.visitPageClicked)

        self.openModDir = qtg.QAction('Open dir...', self)
        self.openModDir.triggered.connect(self.openModDirClicked)

        self.hideMod = qtg.QAction('Hide', self)
        self.hideMod.triggered.connect(self.hideModClicked)

        self.addActions((self.enable, self.disable, self.hideMod, self.delete, self.addSeparator(), self.visitModPage, self.openModDir))
    
    def enabledClicked(self):
        if self.wasLastClickLMB():
            self.qParent.setItemEnabled()
    
    def disabledClicked(self):
        if self.wasLastClickLMB():
            self.qParent.setItemDisabled()
    
    def deleteClicked(self):
        if self.wasLastClickLMB():
            self.qParent.deleteItem()
    
    def visitPageClicked(self):
        if self.wasLastClickLMB():
            self.qParent.visitModPage()
    
    def openModDirClicked(self):
        if self.wasLastClickLMB():
            self.qParent.openModDir()
    
    def hideModClicked(self):
        if self.wasLastClickLMB():
            self.qParent.hideMod()

# EVENT OVERRIDES

    def showEvent(self, event: qtg.QShowEvent) -> None:
        selectedItems = self.qParent.getSelectedNameItems()
        if len(selectedItems) <= 0:
            event.accept()
            return

        if Save().getModworkshopAssetID(selectedItems[0].text()):
            self.visitModPage.setEnabled(True)
        else:
            self.visitModPage.setEnabled(False)

        return super().showEvent(event)
