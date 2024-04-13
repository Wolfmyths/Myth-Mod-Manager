from __future__ import annotations
from typing import TYPE_CHECKING

import PySide6.QtGui as qtg

from src.widgets.QMenu.QMenu import ModContextMenu

if TYPE_CHECKING:
    from src.widgets.modProfileQTreeWidget import ProfileList


class ProfileMenu(ModContextMenu):

    def __init__(self, qParent: ProfileList) -> None:
        super().__init__(qParent)

        self.qParent = qParent

        qParent.profileRightclicked.connect(self.profileRightClicked)
        qParent.modRightclicked.connect(self.modRightClicked)
        qParent.noneRightclicked.connect(self.noneRightClicked)

        self.profileApply = qtg.QAction('Apply Profile', self)
        self.profileAdd = qtg.QAction('Add Profile', self)
        self.profileRemove = qtg.QAction('Remove Profile', self)
        self.profileEdit = qtg.QAction('Change Profile Name', self)
        self.profileCopy = qtg.QAction('Copy Profile', self)
        self.modAdd = qtg.QAction('Add Mods', self)
        self.modRemove = qtg.QAction('Remove Mod', self)
        self.copyModsTo = qtg.QAction('Copy mod(s) to...', self)

        self.profileApply.triggered.connect(lambda: self.callFunc(self.qParent.applyProfileEvent))
        self.profileAdd.triggered.connect(lambda: self.callFunc(self.qParent.menuAddProfile))
        self.profileRemove.triggered.connect(lambda: self.callFunc(self.qParent.deleteProfile))
        self.profileEdit.triggered.connect(lambda: self.callFunc(self.qParent.editProfileMenu))
        self.profileCopy.triggered.connect(lambda: self.callFunc(self.qParent.copyProfile))
        self.modAdd.triggered.connect(lambda: self.callFunc(self.qParent.modAddMenu))
        self.modRemove.triggered.connect(lambda: self.callFunc(self.qParent.removeMods))
        self.copyModsTo.triggered.connect(lambda: self.callFunc(self.qParent.copyModsToProfileMenu))

        self.profileButtons = (self.profileApply, self.modAdd, self.profileAdd, self.profileRemove, self.profileEdit, self.profileCopy, self.copyModsTo)
        self.modButtons = (self.profileApply, self.modAdd, self.modRemove, self.copyModsTo)

        action: qtg.QAction
        for action in self.findChildren(qtg.QAction):
            
            action.installEventFilter(self)
            self.addAction(action)
        
        self.actionsTuple = tuple(self.actions())

    def profileRightClicked(self):
        for action in self.actionsTuple:
            if action in self.profileButtons:
                action.setVisible(True)
            else:
                action.setVisible(False)
    
    def modRightClicked(self):
        for action in self.actionsTuple:
            if action in self.modButtons:
                action.setVisible(True)
            else:
                action.setVisible(False)
    
    def noneRightClicked(self):
        self.profileAdd.setVisible(True)

        for action in self.actionsTuple:
            if action is not self.profileAdd:
                action.setVisible(False)
