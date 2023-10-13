from __future__ import annotations
from typing import TYPE_CHECKING

import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
from PySide6.QtCore import Signal, Qt as qt

from src.widgets.QMenu.ignoreModListQMenu import IgnoredModsQMenu

from src.constant_vars import MOD_IGNORED
from src.save import Save

if TYPE_CHECKING:
    from src.settings import Options

class IgnoredMods(qtw.QListWidget):

    itemsRemoved = Signal()
    itemsChanged = Signal()

    def __init__(self, parent: Options) -> None:
        super().__init__(parent)

        self.saveManager = Save()

        self.contextMenu = IgnoredModsQMenu(self)

        self.setSelectionMode(self.SelectionMode.ExtendedSelection)

    def refreshList(self) -> None:
        self.clear()
        items = [x for x in self.saveManager.sections() if self.saveManager.getboolean(x, MOD_IGNORED, fallback=False)]
        self.addItems(items)
        self.itemsChanged.emit()

    
    def getItems(self) -> list[qtw.QListWidgetItem]:
        return [self.item(x) for x in range(self.count())]

# EVENT OVERRIDES

    def mousePressEvent(self, event: qtg.QMouseEvent) -> None:
        if event.button() == qt.MouseButton.RightButton:
            self.contextMenu.exec(qtg.QCursor.pos())
        return super().mousePressEvent(event)

    def removeItemWidgets(self) -> None:

        itemsInList = self.getItems()

        for item in self.selectedItems():
            self.saveManager[item.text()][MOD_IGNORED] = 'False'

            index = itemsInList.index(item)
            self.takeItem(index)
            itemsInList.pop(index)
        
        self.saveManager.writeData()

        self.itemsRemoved.emit()
        self.itemsChanged.emit()

    def showEvent(self, event: qtg.QShowEvent) -> None:
        self.refreshList()
        return super().showEvent(event)
