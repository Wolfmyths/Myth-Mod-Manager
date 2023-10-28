from typing import TYPE_CHECKING

import PySide6.QtGui as qtg

from src.widgets.QMenu.QMenu import ModContextMenu

if TYPE_CHECKING:
    from src.widgets.ignoredModsQListWidget import IgnoredMods

class IgnoredModsQMenu(ModContextMenu):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.qParent: IgnoredMods = parent

        self.removeItem = qtg.QAction('Remove')
        self.removeItem.triggered.connect(self.removeItemClicked)

        self.addAction(self.removeItem)
    
    def removeItemClicked(self) -> None:
        if self.wasLastClickLMB():
            self.qParent.removeItemWidgets()