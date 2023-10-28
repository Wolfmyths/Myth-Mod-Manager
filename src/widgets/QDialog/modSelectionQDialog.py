import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt as qt

from src.widgets.QDialog.QDialog import Dialog

import src.errorChecking as errorChecking
from src.save import Save
from src.constant_vars import MOD_CONFIG, OPTIONS_CONFIG

class SelectMod(Dialog):

    mods: list[str] = None

    def __init__(self, savePath: str = MOD_CONFIG, optionsPath: str = OPTIONS_CONFIG) -> None:
        super().__init__()

        self.setWindowTitle('Mods to be added:')

        layout = qtw.QVBoxLayout()

        self.modList = qtw.QListWidget(self)
        self.modList.setHorizontalScrollBarPolicy(qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.modList.setFocusPolicy(qt.FocusPolicy.NoFocus)
        self.modList.setSelectionMode(qtw.QListWidget.SelectionMode.MultiSelection)

        self.searchBar = qtw.QLineEdit()
        self.searchBar.setPlaceholderText('Search...')
        self.searchBar.textChanged.connect(lambda x: self.search(x))

        self.saveManager = Save(savePath)

        buttons = qtw.QDialogButtonBox.StandardButton.Ok | qtw.QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = qtw.QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.modList.addItems(sorted([x for x in self.saveManager.mods() if errorChecking.isInstalled(x, optionsPath)]))

        for widget in (self.searchBar, self.modList, self.buttonBox):
            layout.addWidget(widget)
        
        self.setLayout(layout)
    
    def search(self, input: str) -> None:

        results = self.modList.findItems(f'{input}*', qt.MatchFlag.MatchWildcard | qt.MatchFlag.MatchExactly)

        for i in range(0, self.modList.count() + 1):

            item = self.modList.item(i)

            if item not in results:
                self.modList.setRowHidden(i, True)
            else:
                self.modList.setRowHidden(i, False)
    
    def accept(self) -> None:

        self.setResult(1)

        self.mods = [x.text() for x in self.modList.selectedItems()]
        return super().accept()
    
    def reject(self) -> None:
        self.setResult(0)
        return super().reject()

