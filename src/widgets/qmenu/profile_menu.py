from __future__ import annotations
from typing import TYPE_CHECKING

import PySide6.QtGui as qtg
from PySide6.QtCore import QCoreApplication as qapp, Slot
from typing_extensions import override

from src.widgets.qmenu.mod_context_menu import ModContextMenu

if TYPE_CHECKING:
    import PySide6.QtWidgets as qtw


class ProfileMenu(ModContextMenu):

    def __init__(self, qParent: qtw.QWidget | None = None) -> None:
        super().__init__(qParent)

        self.profileApply = qtg.QAction(self)
        self.profileAdd = qtg.QAction(self)
        self.profileRemove = qtg.QAction(self)
        self.profileEdit = qtg.QAction(self)
        self.profileCopy = qtg.QAction(self)
        self.modAdd = qtg.QAction(self)
        self.modRemove = qtg.QAction(self)
        self.copyModsTo = qtg.QAction(self)

        self.profileButtons = (
            self.profileApply, self.modAdd, self.profileAdd, self.profileRemove, self.profileEdit,
            self.profileCopy, self.copyModsTo
        )
        self.modButtons = (
            self.profileApply, self.modAdd, self.modRemove, self.copyModsTo
        )

        action: qtg.QAction
        for action in self.findChildren(qtg.QAction):
            
            action.installEventFilter(self)
            self.addAction(action)
        
        self.actionsTuple = tuple(self.actions())

        self.applyStaticText()

    @override
    def applyStaticText(self) -> None:
        self.profileApply.setText(qapp.translate('ProfileMenu', 'Apply Profile'))
        self.profileAdd.setText(qapp.translate('ProfileMenu', 'Add Profile'))
        self.profileRemove.setText(qapp.translate('ProfileMenu', 'Remove Profile'))
        self.profileEdit.setText(qapp.translate('ProfileMenu', 'Change Profile Name'))
        self.profileCopy.setText(qapp.translate('ProfileMenu', 'Copy Profile'))
        self.modAdd.setText(qapp.translate('ProfileMenu', 'Add Mods'))
        self.modRemove.setText(qapp.translate('ProfileMenu', 'Remove Mod'))
        self.copyModsTo.setText(qapp.translate('ProfileMenu', 'Copy mod(s) to...'))

    @Slot()
    def profileRightClicked(self) -> None:
        for action in self.actionsTuple:
            if action in self.profileButtons:
                action.setVisible(True)
            else:
                action.setVisible(False)
    
    @Slot()
    def modRightClicked(self) -> None:
        for action in self.actionsTuple:
            if action in self.modButtons:
                action.setVisible(True)
            else:
                action.setVisible(False)
    
    @Slot()
    def noneRightClicked(self) -> None:
        self.profileAdd.setVisible(True)

        for action in self.actionsTuple:
            if action is not self.profileAdd:
                action.setVisible(False)
