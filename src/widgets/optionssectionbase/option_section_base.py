import PySide6.QtWidgets as qtw
from PySide6.QtCore import Signal

from src.constant_vars import OptionKeys

class OptionsSectionBase(qtw.QWidget):
    pendingChanges = Signal(OptionKeys, bool)

    def __init__(self, parent: qtw.QWidget | None = None) -> None:
        super().__init__(parent=parent)

    def applyStaticText(self) -> None:
        return