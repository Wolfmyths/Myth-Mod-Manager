
import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
from PySide6.QtCore import Qt as qt

from src.constant_vars import ICON

class Dialog(qtw.QDialog):
    '''Base class for QDialog Objects'''
    def __init__(self, parent: qtw.QWidget | None = None) -> None:
        super().__init__(parent=parent)

        self.setWindowIcon(qtg.QIcon(ICON))
        self.setWindowFlag(qt.WindowType.WindowStaysOnTopHint, True)