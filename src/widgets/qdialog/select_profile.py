import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt as qt, QCoreApplication as qapp, Slot
from typing_extensions import override

from src.widgets.qdialog.dialog import Dialog

from src.helpers.profile_manager import ProfileManager

class SelectProfile(Dialog):

    profile: str = ''

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle(qapp.translate('SelectProfile', 'Profile to copy mod(s) to:'))

        layout = qtw.QVBoxLayout()

        self.profileList = qtw.QListWidget(self)
        self.profileList.setHorizontalScrollBarPolicy(qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.profileList.setFocusPolicy(qt.FocusPolicy.NoFocus)
        self.profileList.setSelectionMode(qtw.QListWidget.SelectionMode.SingleSelection)

        self.searchBar = qtw.QLineEdit()
        self.searchBar.setPlaceholderText(qapp.translate('SelectProfile', 'Search...'))
        self.searchBar.textChanged.connect(self.search)

        buttons = qtw.QDialogButtonBox.StandardButton.Ok | qtw.QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = qtw.QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.profileList.addItems(ProfileManager.get_profile_names())

        for widget in (self.searchBar, self.profileList, self.buttonBox):
            layout.addWidget(widget)
        
        self.setLayout(layout)
    
    @Slot(str)
    def search(self, input: str) -> None:

        results: list[qtw.QListWidgetItem] = self.profileList.findItems(
            f'{input}*',
            qt.MatchFlag.MatchWildcard | qt.MatchFlag.MatchExactly
        )

        for i in range(0, self.profileList.count() + 1):

            item: qtw.QListWidgetItem = self.profileList.item(i)

            if item not in results:
                self.profileList.setRowHidden(i, True)
            else:
                self.profileList.setRowHidden(i, False)
    
    @override
    @Slot()
    def accept(self) -> None:

        self.setResult(1)

        try:
            self.profile = self.profileList.selectedItems()[0].text()
        except IndexError:
            pass

        return super().accept()
    
    @override
    @Slot()
    def reject(self) -> None:
        self.setResult(0)
        return super().reject()
