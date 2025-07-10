from typing import TYPE_CHECKING

import PySide6.QtGui as qtg
from PySide6.QtCore import QCoreApplication as qapp, Slot

from src.widgets.qmenu.QMenu import ModContextMenu

if TYPE_CHECKING:
    from src.widgets.qlistwidget.ignored_mods import IgnoredMods

class IgnoredModsQMenu(ModContextMenu):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.qParent: IgnoredMods = parent

        self.removeItem = qtg.QAction(self)
        self.removeItem.triggered.connect(self.onRemoveItemTriggered)

        self.addAction(self.removeItem)

        self.applyStaticText()
    
    @Slot()
    def onRemoveItemTriggered(self) -> None:
        self.callFunc(self.qParent.removeItemWidgets)

    def applyStaticText(self) -> None:
        self.removeItem.setText(qapp.translate('IgnoredModsQMenu', 'Remove'))