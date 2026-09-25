from __future__ import annotations
from typing import TYPE_CHECKING

import PySide6.QtGui as qtg
from PySide6.QtCore import QCoreApplication as qapp
from typing_extensions import override

from src.widgets.qmenu.mod_context_menu import ModContextMenu

if TYPE_CHECKING:
    import PySide6.QtWidgets as qtw

class TagViewerMenu(ModContextMenu):
    def __init__(self, qParent: qtw.QWidget | None = None) -> None:
        super().__init__(qParent)

        self.addTag = qtg.QAction(self)

        self.removeTag = qtg.QAction(self)

        self.deleteAllTags = qtg.QAction(self)

        self.addActions((self.addTag, self.removeTag, self.deleteAllTags))

        self.applyStaticText()

    @override
    def applyStaticText(self) -> None:
        self.addTag.setText(qapp.translate('TagViewerMenu', 'Add Tag(s)'))
        self.removeTag.setText(qapp.translate('TagViewerMenu', 'Remove Tag(s)'))
        self.deleteAllTags.setText(qapp.translate('TagViewerMenu', 'Delete All Tags'))