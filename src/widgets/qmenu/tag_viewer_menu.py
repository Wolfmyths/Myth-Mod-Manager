from __future__ import annotations
from typing import TYPE_CHECKING

import PySide6.QtGui as qtg
from PySide6.QtCore import QCoreApplication as qapp, Slot

from src.widgets.qmenu.QMenu import ModContextMenu

if TYPE_CHECKING:
    from src.widgets.qwidget.tag_viewer import TagViewer

class TagViewerMenu(ModContextMenu):
    def __init__(self, qParent: TagViewer) -> None:
        super().__init__(qParent)

        self.qParent: TagViewer = qParent

        self.addTag = qtg.QAction(self)
        self.addTag.triggered.connect(self.onAddTagTriggered)

        self.removeTag = qtg.QAction(self)
        self.removeTag.triggered.connect(self.onRemoveTagTriggered)

        self.deleteAllTags = qtg.QAction(self)
        self.deleteAllTags.triggered.connect(self.onDeleteAllTagsTriggered)

        self.addActions((self.addTag, self.removeTag, self.deleteAllTags))

        self.applyStaticText()

    @Slot()
    def onAddTagTriggered(self) -> None:
        self.callFunc(self.qParent.addTags)

    @Slot()
    def onRemoveTagTriggered(self) -> None:
        self.callFunc(self.qParent.removeTags)

    @Slot()
    def onDeleteAllTagsTriggered(self) -> None:
        self.callFunc(self.qParent.deleteAllTags)

    def applyStaticText(self) -> None:
        self.addTag.setText(qapp.translate('TagViewerMenu', 'Add Tag(s)'))
        self.removeTag.setText(qapp.translate('TagViewerMenu', 'Remove Tag(s)'))
        self.deleteAllTags.setText(qapp.translate('TagViewerMenu', 'Delete All Tags'))