import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt as qt

from widgets.QDialog.QDialog import Dialog
import errorChecking

from save import Save

class SelectMod(Dialog):

    mods: list[str] = None

    def __init__(self) -> None:
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

        saveManager = Save()

        buttons = qtw.QDialogButtonBox.StandardButton.Ok | qtw.QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = qtw.QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(lambda: self.accept())
        self.buttonBox.rejected.connect(lambda: self.reject())

        self.modList.addItems([x for x in sorted(saveManager.sections()) if errorChecking.isInstalled(x)])

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

