import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
from PySide6.QtCore import Signal, Qt as qt, Slot
from typing_extensions import override

from src.helpers.save_manager import Save
from src.widgets.qmenu.ignored_mods import IgnoredModsQMenu
    

class IgnoredMods(qtw.QListWidget):

    itemsRemoved = Signal()
    itemsChanged = Signal()

    def __init__(self, parent: qtw.QWidget | None = None) -> None:
        super().__init__(parent)

        self.contextMenu = IgnoredModsQMenu(self)

        self.contextMenu.removeItem.triggered.connect(self.removeItemWidgets)

        self.setSelectionMode(self.SelectionMode.ExtendedSelection)

    @Slot()
    def refreshList(self) -> None:
        self.clear()
        items: list[str] = [
            x for x in Save.mods() if Save.getIgnored(x)
        ]
        self.addItems(items)
        self.itemsChanged.emit()

    
    def getItems(self) -> list[qtw.QListWidgetItem]:
        return [self.item(x) for x in range(self.count())]

# EVENT OVERRIDES

    @override
    def mousePressEvent(self, event: qtg.QMouseEvent) -> None:
        if event.button() == qt.MouseButton.RightButton:
            self.contextMenu.exec(qtg.QCursor.pos())
        return super().mousePressEvent(event)

    def removeItemWidgets(self) -> None:

        itemsInList: list[qtw.QListWidgetItem] = self.getItems()

        for item in self.selectedItems():
            Save.setIgnored(item.text(), False)

            index: int = itemsInList.index(item)
            self.takeItem(index)
            itemsInList.pop(index)
        
        Save.saveJSON()

        self.itemsRemoved.emit()
        self.itemsChanged.emit()

    @override
    def showEvent(self, event: qtg.QShowEvent) -> None:
        self.refreshList()
        return super().showEvent(event)
