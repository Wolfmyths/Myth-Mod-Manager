
import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt as qt

from widgets.QDialog.QDialog import Dialog

from profileManager import ProfileManager

class SelectProfile(Dialog):

    profile: str = None

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle('Profile to copy mod(s) to:')

        layout = qtw.QVBoxLayout()

        self.profileList = qtw.QListWidget(self)
        self.profileList.setHorizontalScrollBarPolicy(qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.profileList.setFocusPolicy(qt.FocusPolicy.NoFocus)
        self.profileList.setSelectionMode(qtw.QListWidget.SelectionMode.SingleSelection)

        self.searchBar = qtw.QLineEdit()
        self.searchBar.setPlaceholderText('Search...')
        self.searchBar.textChanged.connect(lambda x: self.search(x))

        profileManager = ProfileManager()

        buttons = qtw.QDialogButtonBox.StandardButton.Ok | qtw.QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = qtw.QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(lambda: self.accept())
        self.buttonBox.rejected.connect(lambda: self.reject())

        self.profileList.addItems(list(profileManager.getJSON().keys()))

        for widget in (self.searchBar, self.profileList, self.buttonBox):
            layout.addWidget(widget)
        
        self.setLayout(layout)
    
    def search(self, input: str) -> None:

        results = self.profileList.findItems(f'{input}*', qt.MatchFlag.MatchWildcard | qt.MatchFlag.MatchExactly)

        for i in range(0, self.profileList.count() + 1):

            item = self.profileList.item(i)

            if item not in results:
                self.profileList.setRowHidden(i, True)
            else:
                self.profileList.setRowHidden(i, False)
    
    def accept(self) -> None:

        self.setResult(1)

        try:
            self.profile = self.profileList.selectedItems()[0].text()
        except IndexError:
            pass

        return super().accept()
    
    def reject(self) -> None:
        self.setResult(0)
        return super().reject()
