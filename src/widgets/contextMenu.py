
import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw

class ModContextMenu(qtw.QMenu):
    def __init__(self, parent: qtw.QListWidget) -> None:
        super().__init__()
    
    def showEvent(self, event: qtg.QShowEvent) -> None:

        self.move(qtg.QCursor.pos())

        return super().showEvent(event)