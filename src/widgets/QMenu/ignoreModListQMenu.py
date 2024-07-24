from typing import TYPE_CHECKING

import PySide6.QtGui as qtg
from PySide6.QtCore import QCoreApplication as qapp

from src.widgets.QMenu.QMenu import ModContextMenu

if TYPE_CHECKING:
    from src.widgets.ignoredModsQListWidget import IgnoredMods

class IgnoredModsQMenu(ModContextMenu):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.qParent: IgnoredMods = parent

        self.removeItem = qtg.QAction(self)
        self.removeItem.triggered.connect(lambda: self.callFunc(self.qParent.removeItemWidgets))

        self.addAction(self.removeItem)

        self.applyStaticText()

    def applyStaticText(self) -> None:
        self.removeItem.setText(qapp.translate('IgnoredModsQMenu', 'Remove'))