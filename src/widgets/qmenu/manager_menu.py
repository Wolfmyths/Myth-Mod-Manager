from __future__ import annotations
from typing import TYPE_CHECKING

import PySide6.QtGui as qtg
from PySide6.QtCore import QCoreApplication as qapp, Slot
from PySide6.QtWidgets import QTableWidgetItem

from src.helpers.save_manager import Save
from src.widgets.qmenu.mod_context_menu import ModContextMenu

if TYPE_CHECKING:
    from src.widgets.qtable.mod_list_widget import ModListWidget

class ManagerMenu(ModContextMenu):
    def __init__(self, qParent: ModListWidget) -> None:
        super().__init__(qParent)

        self.qParent: ModListWidget = qParent

        self.enable = qtg.QAction(self)
        self.enable.triggered.connect(self.onEnableTriggered)

        self.disable = qtg.QAction(self)
        self.disable.triggered.connect(self.onDisableTriggered)

        self.delete = qtg.QAction(self)
        self.delete.triggered.connect(self.onDeleteTriggered)

        self.checkUpdate = qtg.QAction(self)
        self.checkUpdate.triggered.connect(self.onCheckUpdateTriggered)

        self.visitModPage = qtg.QAction(self)
        self.visitModPage.triggered.connect(self.onVisitModPageTriggered)

        self.openModDir = qtg.QAction(self)
        self.openModDir.triggered.connect(self.onOpenModDirTriggered)

        self.hideMod = qtg.QAction(self)
        self.hideMod.triggered.connect(self.onHideModTriggered)

        self.viewTags = qtg.QAction(self)
        self.viewTags.triggered.connect(self.onViewTagsTriggered)

        self.addActions((self.enable, self.disable, self.hideMod, self.delete, self.addSeparator(),
                         self.visitModPage, self.checkUpdate, self.openModDir, self.addSeparator(),
                         self.viewTags))

        self.applyStaticText()

    @Slot()
    def onEnableTriggered(self) -> None:
        self.callFunc(self.qParent.setItemEnabled)
    
    @Slot()
    def onDisableTriggered(self) -> None:
        self.callFunc(self.qParent.setItemDisabled)

    @Slot()
    def onDeleteTriggered(self) -> None:
        self.callFunc(self.qParent.deleteItem)

    @Slot()
    def onCheckUpdateTriggered(self) -> None:
        self.callFunc(self.qParent.checkModUpdate)
    
    @Slot()
    def onVisitModPageTriggered(self) -> None:
        self.callFunc(self.qParent.visitModPage)

    @Slot()
    def onOpenModDirTriggered(self) -> None:
        self.callFunc(self.qParent.openModDir)

    @Slot()
    def onHideModTriggered(self) -> None:
        self.callFunc(self.qParent.hideMod)

    @Slot()
    def onViewTagsTriggered(self) -> None:
        self.callFunc(self.qParent.viewTags)

    def applyStaticText(self) -> None:
        self.enable.setText(qapp.translate('ManagerMenu', 'Enable'))
        self.disable.setText(qapp.translate('ManagerMenu', 'Disable'))
        self.delete.setText(qapp.translate('ManagerMenu', 'Delete'))
        self.checkUpdate.setText(qapp.translate('ManagerMenu', 'Check Update'))
        self.visitModPage.setText(qapp.translate('ManagerMenu', 'Visit Page'))
        self.openModDir.setText(qapp.translate('ManagerMenu', 'Open Folder...'))
        self.hideMod.setText(qapp.translate('ManagerMenu', 'Hide'))
        self.viewTags.setText(qapp.translate('ManagerMenu', 'View Tag(s)'))

# EVENT OVERRIDES

    def showEvent(self, event: qtg.QShowEvent) -> None:
        selectedItems: list[QTableWidgetItem] = self.qParent.getSelectedNameItems()
        if len(selectedItems) <= 0:
            event.accept()
            return

        if Save.getModworkshopAssetID(selectedItems[0].text()):
            self.visitModPage.setEnabled(True)
            self.checkUpdate.setEnabled(True)
        else:
            self.visitModPage.setEnabled(False)
            self.checkUpdate.setEnabled(False)

        return super().showEvent(event)
