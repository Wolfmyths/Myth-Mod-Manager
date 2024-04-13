from __future__ import annotations
from typing import TYPE_CHECKING

import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
from PySide6.QtCore import Qt as qt

if TYPE_CHECKING:
    from src.widgets.tagViewerQWidget import TagViewer

class TagDisplay(qtw.QTableWidget):
    def __init__(self, parent: TagViewer) -> None:
        super().__init__(parent=parent)

        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(('Name', 'Tags'))
        self.verticalHeader().hide()
        self.setEditTriggers(qtw.QAbstractItemView.EditTrigger.NoEditTriggers)

        self.setColumnWidth(0, 400)
        self.setColumnWidth(1, 400)

        self.setSelectionBehavior(qtw.QAbstractItemView.SelectionBehavior.SelectRows)

        horizontalHeader = self.horizontalHeader()
        horizontalHeader.setSectionResizeMode(0, qtw.QHeaderView.ResizeMode.ResizeToContents)
        horizontalHeader.setSectionResizeMode(1, qtw.QHeaderView.ResizeMode.Stretch)
    
    # EVENT OVERRIDES
    def mousePressEvent(self, event: qtg.QMouseEvent) -> None:
        if event.button() == qt.MouseButton.RightButton:
            parent: TagViewer = self.parent()
        
            # Will return None if there are no mods causing a traceback
            tableWidgetItem = self.itemAt(event.pos())

            if tableWidgetItem is not None:

                if len(self.selectedItems()[::self.columnCount()]) <= 1:
                    self.selectRow(tableWidgetItem.row())
                parent.contextMenu.exec(qtg.QCursor.pos())

        return super().mousePressEvent(event)