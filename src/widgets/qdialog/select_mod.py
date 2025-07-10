from typing import List
import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt as qt, QCoreApplication as qapp, Slot

from src.widgets.qdialog.dialog import Dialog

import src.helpers.helper as helper
from src.helpers.save_manager import Save
from src.constant_vars import ModRole

class SelectMod(Dialog):

    mods: list[str] = None

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle(qapp.translate('SelectMod', 'Mods to be added:'))

        layout = qtw.QVBoxLayout()

        self.modList = qtw.QListWidget(self)
        self.modList.setHorizontalScrollBarPolicy(qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.modList.setFocusPolicy(qt.FocusPolicy.NoFocus)
        self.modList.setSelectionMode(qtw.QListWidget.SelectionMode.MultiSelection)

        self.searchBar = qtw.QLineEdit()
        self.searchBar.setPlaceholderText(qapp.translate('SelectMod', 'Search... use "tag:" with no spaces to search for tags, use a comma "," to seperate tags'))
        self.searchBar.textChanged.connect(self.search)

        buttons = qtw.QDialogButtonBox.StandardButton.Ok | qtw.QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = qtw.QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Add mods
        self.modList.addItems(sorted([x for x in Save.mods() if helper.isInstalled(x)]))

        # Add tags
        for i in range(self.modList.count()):
            item: qtw.QListWidgetItem = self.modList.item(i)
            modTags: list[str] = Save.getTags(item.text())
            if modTags is not None:
                item.setData(ModRole.tags, modTags)

        for widget in (self.searchBar, self.modList, self.buttonBox):
            layout.addWidget(widget)
        
        self.setLayout(layout)
    
    @Slot(str)
    def search(self, input: str) -> None:
        searchedTags = None

        if input.startswith('tag:') and len(input) > 4:
            splitStr: list[str] = input.split(' ')
            input = ' '.join(splitStr[1:])
            searchedTags: list[str] = splitStr[0][4:].split(',')


        results: List[qtw.QListWidgetItem] = self.modList.findItems(
            f'{input}*',
            qt.MatchFlag.MatchWildcard | qt.MatchFlag.MatchExactly
        )

        for i in range(self.modList.count()):

            item: qtw.QListWidgetItem = self.modList.item(i)
            if item is not None:
                modTags: tuple[str] | None = item.data(ModRole.tags)

            if searchedTags is not None and modTags is not None:
                for tag in searchedTags:
                    if tag in modTags and item in results:
                        self.modList.setRowHidden(i, False)
                    else:
                        self.modList.setRowHidden(i, True)
            else:
                if item in results and searchedTags is None:
                    self.modList.setRowHidden(i, False)
                else:
                    self.modList.setRowHidden(i, True)
    
    @Slot()
    def accept(self) -> None:

        self.setResult(1)

        self.mods = [x.text() for x in self.modList.selectedItems()]
        return super().accept()
    
    @Slot()
    def reject(self) -> None:
        self.setResult(0)
        return super().reject()

