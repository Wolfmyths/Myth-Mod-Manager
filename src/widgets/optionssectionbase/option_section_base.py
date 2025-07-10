from __future__ import annotations
from typing import TYPE_CHECKING

import PySide6.QtWidgets as qtw
from PySide6.QtCore import Signal

from src.constant_vars import OptionKeys

if TYPE_CHECKING:
    from src.widgets.qwidget.options import Options

class OptionsSectionBase(qtw.QWidget):
    pendingChanges = Signal(OptionKeys, bool)

    def __init__(self, parent: Options = None) -> None:
        super().__init__(parent=parent)

    def applyStaticText(self) -> None:
        return