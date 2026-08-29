from typing import cast

import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
from PySide6.QtCore import Signal, QCoreApplication as qapp, Slot

from src.constant_vars import ModRole, PROGRAM_NAME, ICON
from src.helpers.save_manager import Save
from src.widgets.qmenu.tag_viewer_menu import TagViewerMenu
from src.widgets.qdialog.tag_handler import TagHandler
from src.widgets.qtable.tag_display import TagDisplay
from src.widgets.qdialog.confirmation import Confirmation

class TagViewer(qtw.QWidget):
    tagChanged = Signal(str, tuple[str])
    def __init__(self, parent: qtw.QWidget | None = None) -> None:
        super().__init__(parent = parent)

        self.setWindowIcon(qtg.QIcon(ICON))

        layout = qtw.QVBoxLayout()

        self.contextMenu = TagViewerMenu(self)
        self.tagQTable = TagDisplay(self.contextMenu, self)

        self.contextMenu.addTag.triggered.connect(self.addTags)
        self.contextMenu.removeTag.triggered.connect(self.removeTags)
        self.contextMenu.deleteAllTags.triggered.connect(self.deleteAllTags)

        self.refreshTable()

        self.resize(800, 900)

        for widget in (self.tagQTable, ):
            layout.addWidget(widget)
        
        self.setLayout(layout)
        self.applyStaticText()
    
    def applyStaticText(self) -> None:
        self.setWindowTitle(f'{PROGRAM_NAME}: ' + qapp.translate('TagViewer', 'Mod Tag Viewer'))
    
    @Slot()
    def deleteAllTags(self) -> None:
        confirmation = Confirmation(
            qapp.translate('TagViewer', 'Delete all tags'),
            qapp.translate('TagViewer', 'Are you sure you want to delete all of the tags associated with your mods?') +
            '\n' +
            qapp.translate('TagViewer', '(This action cannot be reversed)')
        )
        confirmation.exec()
        if confirmation.result():
            Save.clearTags()
            Save.saveJSON()
    
    @Slot()
    def addTags(self) -> None:
        items = self.tagQTable.selectedItems()[::self.tagQTable.columnCount()]
        allTags = Save.getAllTags()

        tagQDialog = TagHandler(1, allTags)
        tagQDialog.exec()
        if tagQDialog.result():
            modsToBeChanged = [x.text() for x in items]
            tagsToBeAdded = tagQDialog.input.text().split(',')
            Save.setTags(tagsToBeAdded, *modsToBeChanged)
            Save.saveJSON()

            # Apply changes to GUI
            for mod in modsToBeChanged:
                self.tagChanged.emit(mod, tuple(Save.getTags(mod)))

            self.refreshTable()
    
    @Slot()
    def removeTags(self) -> None:
        items = self.tagQTable.selectedItems()[::self.tagQTable.columnCount()]
        allTags = Save.getAllTags()

        tagQDialog = TagHandler(0, allTags)
        tagQDialog.exec()

        if tagQDialog.result():
            modsToBeChanged = [x.text() for x in items]
            tagsToBeRemoved = tagQDialog.input.text().split(',')

            Save.removeTags(tagsToBeRemoved, *modsToBeChanged)
            Save.saveJSON()

            # Apply changes to GUI
            for mod in modsToBeChanged:
                self.tagChanged.emit(mod, tuple(Save.getTags(mod)))

            self.refreshTable()

    def refreshTable(self) -> None:
        if self.parent() is None:
            return

        manager_table = cast(qtw.QTableWidget, self.parent())

        if self.tagQTable.rowCount() > 0:
            self.tagQTable.setRowCount(0)

        for i in range(manager_table.rowCount()):
            modNameItem = manager_table.item(i, 0)

            modTagsData: tuple[str] | None = modNameItem.data(ModRole.tags)

            if modTagsData is None:
                modTagsData = tuple[str]()
            
            self.tagQTable.insertRow(i)

            modName = qtw.QTableWidgetItem(modNameItem.text())
            modTags = qtw.QTableWidgetItem(', '.join(modTagsData))

            self.tagQTable.setItem(i, 0, modName)
            self.tagQTable.setItem(i, 1, modTags)
