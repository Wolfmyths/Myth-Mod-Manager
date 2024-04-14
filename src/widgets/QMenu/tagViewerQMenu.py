from __future__ import annotations
from typing import TYPE_CHECKING

import PySide6.QtGui as qtg

from src.widgets.QMenu.QMenu import ModContextMenu

if TYPE_CHECKING:
    from src.widgets.tagViewerQWidget import TagViewer

class TagViewerMenu(ModContextMenu):
    def __init__(self, qParent: TagViewer) -> None:
        super().__init__(qParent)

        self.qParent = qParent

        self.addTag = qtg.QAction('Add Tag(s)', self)
        self.addTag.triggered.connect(lambda: self.callFunc(self.qParent.addTags))

        self.removeTag = qtg.QAction('Remove Tag(s)', self)
        self.removeTag.triggered.connect(lambda: self.callFunc(self.qParent.removeTags))

        self.deleteAllTags = qtg.QAction('Delete All Tags', self)
        self.deleteAllTags.triggered.connect(lambda: self.callFunc(self.qParent.deleteAllTags))

        self.addActions((self.addTag, self.removeTag, self.deleteAllTags))
