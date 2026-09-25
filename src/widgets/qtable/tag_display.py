import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
from PySide6.QtCore import Qt as qt, QCoreApplication as qapp
from typing_extensions import override

class TagDisplay(qtw.QTableWidget):
    def __init__(self, context_menu: qtw.QMenu | None = None, parent: qtw.QWidget | None = None) -> None:
        super().__init__(parent=parent)
        
        self.context_menu = context_menu

        self.setColumnCount(2)
        self.verticalHeader().hide()
        self.setEditTriggers(qtw.QAbstractItemView.EditTrigger.NoEditTriggers)

        self.setColumnWidth(0, 400)
        self.setColumnWidth(1, 400)

        self.setSelectionBehavior(qtw.QAbstractItemView.SelectionBehavior.SelectRows)

        horizontalHeader: qtw.QHeaderView = self.horizontalHeader()
        horizontalHeader.setSectionResizeMode(0, qtw.QHeaderView.ResizeMode.ResizeToContents)
        horizontalHeader.setSectionResizeMode(1, qtw.QHeaderView.ResizeMode.Stretch)

        self.applyStaticText()
    
    def applyStaticText(self) -> None:
        self.setHorizontalHeaderLabels(
            (
                qapp.translate('TagDisplay', 'Name'),
                qapp.translate('TagDisplay', 'Tags')
            )
        )
    
    # EVENT OVERRIDES
    @override
    def mousePressEvent(self, event: qtg.QMouseEvent) -> None:
        if event.button() == qt.MouseButton.RightButton:
        
            # Will return None if there are no mods causing a traceback
            tableWidgetItem: qtw.QTableWidgetItem | None = self.itemAt(event.pos())

            if tableWidgetItem is not None:

                if len(self.selectedItems()[::self.columnCount()]) <= 1:
                    self.selectRow(tableWidgetItem.row())
                self.context_menu.exec(qtg.QCursor.pos())

        return super().mousePressEvent(event)