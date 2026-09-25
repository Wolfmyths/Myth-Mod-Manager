from __future__ import annotations
from typing import TYPE_CHECKING

import PySide6.QtGui as qtg
from PySide6.QtCore import QCoreApplication as qapp
from typing_extensions import override

from src.widgets.qmenu.mod_context_menu import ModContextMenu

if TYPE_CHECKING:
    import PySide6.QtWidgets as qtw

class IgnoredModsQMenu(ModContextMenu):
    def __init__(self, parent: qtw.QWidget | None = None) -> None:
        super().__init__(parent)

        self.removeItem = qtg.QAction(self)

        self.addAction(self.removeItem)

        self.applyStaticText()

    @override
    def applyStaticText(self) -> None:
        self.removeItem.setText(qapp.translate('IgnoredModsQMenu', 'Remove'))