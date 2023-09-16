from __future__ import annotations
from typing import TYPE_CHECKING

import PySide6.QtGui as qtg

from widgets.QMenu.QMenu import ModContextMenu

if TYPE_CHECKING:
    from widgets.managerQTableWidget import ModListWidget

class ManagerMenu(ModContextMenu):
    def __init__(self, qParent: ModListWidget) -> None:
        super().__init__(qParent)

        self.qParent = qParent

        self.enable = qtg.QAction('Enable', self)
        self.enable.triggered.connect(lambda: self.enabledClicked())

        self.disable = qtg.QAction('Disable', self)
        self.disable.triggered.connect(lambda: self.disabledClicked())

        self.delete = qtg.QAction('Delete Mod', self)
        self.delete.triggered.connect(lambda: self.deleteClicked())

        self.addActions((self.enable, self.disable, self.delete))
    
    def enabledClicked(self):
        if self.wasLastClickLMB():
            self.qParent.setItemEnabled()
    
    def disabledClicked(self):
        if self.wasLastClickLMB():
            self.qParent.setItemDisabled()
    
    def deleteClicked(self):
        if self.wasLastClickLMB():
            self.qParent.deleteItem()