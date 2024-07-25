from __future__ import annotations
from typing import TYPE_CHECKING

import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
from PySide6.QtCore import Signal, QCoreApplication as qapp

from src.constant_vars import ModRole, PROGRAM_NAME, ICON
from src.widgets.QMenu.tagViewerQMenu import TagViewerMenu
from src.widgets.QDialog.tagHandlerQDialog import TagHandler
from src.widgets.tagDisplayQTable import TagDisplay
from src.widgets.QDialog.deleteWarningQDialog import Confirmation

if TYPE_CHECKING:
    from src.widgets.managerQTableWidget import ModListWidget

class TagViewer(qtw.QWidget):
    tagChanged = Signal(str, tuple)
    def __init__(self, managerTable: ModListWidget = None) -> None:
        super().__init__()
        self.managerTable = managerTable

        self.setWindowIcon(qtg.QIcon(ICON))

        layout = qtw.QVBoxLayout()

        self.tagQTable = TagDisplay(self)
        self.contextMenu = TagViewerMenu(self)

        self.refreshTable()

        self.resize(800, 900)

        for widget in (self.tagQTable, ):
            layout.addWidget(widget)
        
        self.setLayout(layout)
        self.applyStaticText()
    
    def applyStaticText(self) -> None:
        self.setWindowTitle(f'{PROGRAM_NAME}: ' + qapp.translate('TagViewer', 'Mod Tag Viewer'))
    
    def deleteAllTags(self) -> None:
        confirmation = Confirmation(
            qapp.translate('TagViewer', 'Delete all tags'),
            qapp.translate('TagViewer', 'Are you sure you want to delete all of the tags associated with your mods?') +
            '\n' +
            qapp.translate('TagViewer', '(This action cannot be reversed)')
        )
        confirmation.exec()
        if confirmation.result():
            self.managerTable.saveManager.clearTags()
            self.managerTable.saveManager.saveJSON()
    
    def addTags(self) -> None:
        items = self.tagQTable.selectedItems()[::self.tagQTable.columnCount()]
        allTags = self.managerTable.saveManager.getAllTags()

        tagQDialog = TagHandler(1, allTags)
        tagQDialog.exec()
        if tagQDialog.result():
            modsToBeChanged = [x.text() for x in items]
            tagsToBeAdded = tagQDialog.input.text().split(',')
            self.managerTable.saveManager.setTags(tagsToBeAdded, *modsToBeChanged)
            self.managerTable.saveManager.saveJSON()

            # Apply changes to GUI
            for mod in modsToBeChanged:
                self.tagChanged.emit(mod, tuple(self.managerTable.saveManager.getTags(mod)))

            self.refreshTable()
    
    def removeTags(self) -> None:
        items = self.tagQTable.selectedItems()[::self.tagQTable.columnCount()]
        allTags = self.managerTable.saveManager.getAllTags()

        tagQDialog = TagHandler(0, allTags)
        tagQDialog.exec()

        if tagQDialog.result():
            modsToBeChanged = [x.text() for x in items]
            tagsToBeRemoved = tagQDialog.input.text().split(',')

            self.managerTable.saveManager.removeTags(tagsToBeRemoved, *modsToBeChanged)
            self.managerTable.saveManager.saveJSON()

            # Apply changes to GUI
            for mod in modsToBeChanged:
                self.tagChanged.emit(mod, tuple(self.managerTable.saveManager.getTags(mod)))

            self.refreshTable()

    def refreshTable(self) -> None:
        if self.tagQTable.rowCount() > 0:
            self.tagQTable.setRowCount(0)

        for i in range(self.managerTable.rowCount()):
            modNameItem = self.managerTable.item(i, 0)
            modTagsData: tuple[str] = modNameItem.data(ModRole.tags)

            # TODO: Figure out what the point of this codeblock is, IDE says code is unreachable
            if modTagsData is None:
                modTagsData = ()
            
            self.tagQTable.insertRow(i)

            modName = qtw.QTableWidgetItem(modNameItem.text())
            modTags = qtw.QTableWidgetItem(', '.join(modTagsData))

            self.tagQTable.setItem(i, 0, modName)
            self.tagQTable.setItem(i, 1, modTags)
