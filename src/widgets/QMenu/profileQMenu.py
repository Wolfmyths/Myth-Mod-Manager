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

        self.profileApply.triggered.connect(self.profileApplyPressed)
        self.profileAdd.triggered.connect(self.profileAddPressed)
        self.profileRemove.triggered.connect(self.profileRemovePressed)
        self.profileEdit.triggered.connect(self.profileEditPressed)
        self.profileCopy.triggered.connect(self.profileCopyPressed)
        self.modAdd.triggered.connect(self.modAddPressed)
        self.modRemove.triggered.connect(self.modRemovePressed)
        self.copyModsTo.triggered.connect(self.copyModsToPressed)

        self.profileButtons = (self.profileApply, self.modAdd, self.profileAdd, self.profileRemove, self.profileEdit, self.profileCopy, self.copyModsTo)
        self.modButtons = (self.profileApply, self.modAdd, self.modRemove, self.copyModsTo)

        action: qtg.QAction
        for action in self.findChildren(qtg.QAction):
            
            action.installEventFilter(self)
            self.addAction(action)
        
        self.actionsTuple = tuple(self.actions())
    
    def profileApplyPressed(self):
        if self.wasLastClickLMB():
            self.qParent.applyProfileEvent()

    def profileAddPressed(self):
        if self.wasLastClickLMB():
            self.qParent.menuAddProfile()
    
    def profileRemovePressed(self):
        if self.wasLastClickLMB():
            self.qParent.deleteProfile()
    
    def profileEditPressed(self):
        if self.wasLastClickLMB():
            self.qParent.editProfileMenu()
    
    def profileCopyPressed(self):
        if self.wasLastClickLMB():
            self.qParent.copyProfile()
    
    def modAddPressed(self):
        if self.wasLastClickLMB():
            self.qParent.modAddMenu()
    
    def modRemovePressed(self):
        if self.wasLastClickLMB():
            self.qParent.removeMods()
    
    def copyModsToPressed(self):
        if self.wasLastClickLMB():
            self.qParent.copyModsToProfileMenu()

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
