from __future__ import annotations
from typing import TYPE_CHECKING

import PySide6.QtGui as qtg
from PySide6.QtCore import QCoreApplication as qapp

from src.widgets.QMenu.QMenu import ModContextMenu

if TYPE_CHECKING:
    from src.widgets.tagViewerQWidget import TagViewer

class TagViewerMenu(ModContextMenu):
    def __init__(self, qParent: TagViewer) -> None:
        super().__init__(qParent)

        self.qParent = qParent

        self.addTag = qtg.QAction(self)
        self.addTag.triggered.connect(lambda: self.callFunc(self.qParent.addTags))

        self.removeTag = qtg.QAction(self)
        self.removeTag.triggered.connect(lambda: self.callFunc(self.qParent.removeTags))

        self.deleteAllTags = qtg.QAction(self)
        self.deleteAllTags.triggered.connect(lambda: self.callFunc(self.qParent.deleteAllTags))

        self.addActions((self.addTag, self.removeTag, self.deleteAllTags))

        self.applyStaticText()

    def applyStaticText(self) -> None:
        self.addTag.setText(qapp.translate('TagViewerMenu', 'Add Tag(s)'))
        self.removeTag.setText(qapp.translate('TagViewerMenu', 'Remove Tag(s)'))
        self.deleteAllTags.setText(qapp.translate('TagViewerMenu', 'Delete All Tags'))