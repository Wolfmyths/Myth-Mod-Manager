from __future__ import annotations
from typing import TYPE_CHECKING

import PySide6.QtGui as qtg
from PySide6.QtCore import QCoreApplication as qapp, Slot

from src.widgets.qmenu.QMenu import ModContextMenu

if TYPE_CHECKING:
    from src.widgets.qtreewidget.profile_list import ProfileList


class ProfileMenu(ModContextMenu):

    def __init__(self, qParent: ProfileList) -> None:
        super().__init__(qParent)

        self.qParent: ProfileList = qParent

        qParent.profileRightclicked.connect(self.profileRightClicked)
        qParent.modRightclicked.connect(self.modRightClicked)
        qParent.noneRightclicked.connect(self.noneRightClicked)

        self.profileApply = qtg.QAction(self)
        self.profileAdd = qtg.QAction(self)
        self.profileRemove = qtg.QAction(self)
        self.profileEdit = qtg.QAction(self)
        self.profileCopy = qtg.QAction(self)
        self.modAdd = qtg.QAction(self)
        self.modRemove = qtg.QAction(self)
        self.copyModsTo = qtg.QAction(self)

        self.profileApply.triggered.connect(self.onProfileApplyTriggered)
        self.profileAdd.triggered.connect(self.onProfileAddTriggered)
        self.profileRemove.triggered.connect(self.onProfileRemoveTriggered)
        self.profileEdit.triggered.connect(self.onProfileEditTriggered)
        self.profileCopy.triggered.connect(self.onProfileCopyTriggered)
        self.modAdd.triggered.connect(self.onModAddTriggered)
        self.modRemove.triggered.connect(self.onModRemoveTriggered)
        self.copyModsTo.triggered.connect(self.onCopyModsToTriggered)

        self.profileButtons: tuple = (
            self.profileApply, self.modAdd, self.profileAdd, self.profileRemove, self.profileEdit,
            self.profileCopy, self.copyModsTo
        )
        self.modButtons: tuple = (
            self.profileApply, self.modAdd, self.modRemove, self.copyModsTo
        )

        action: qtg.QAction
        for action in self.findChildren(qtg.QAction):
            
            action.installEventFilter(self)
            self.addAction(action)
        
        self.actionsTuple = tuple(self.actions())

        self.applyStaticText()

    @Slot()
    def onProfileApplyTriggered(self) -> None:
        self.callFunc(self.qParent.applyProfileEvent)

    @Slot()
    def onProfileAddTriggered(self) -> None:
        self.callFunc(self.qParent.menuAddProfile)

    @Slot()
    def onProfileRemoveTriggered(self) -> None:
        self.callFunc(self.qParent.deleteProfile)

    @Slot()
    def onProfileEditTriggered(self) -> None:
        self.callFunc(self.qParent.editProfileMenu)

    @Slot()
    def onProfileCopyTriggered(self) -> None:
        self.callFunc(self.qParent.copyProfile)

    @Slot()
    def onModAddTriggered(self) -> None:
        self.callFunc(self.qParent.modAddMenu)

    @Slot()
    def onModRemoveTriggered(self) -> None:
        self.callFunc(self.qParent.removeMods)

    @Slot()
    def onCopyModsToTriggered(self) -> None:
        self.callFunc(self.qParent.copyModsToProfileMenu)

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
