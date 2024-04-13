import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt as qt

from src.widgets.QDialog.QDialog import Dialog

class TagHandler(Dialog):

    # Modes
    REMOVE = 0
    ADD = 1

    def __init__(self, mode: int, allTags: list[str]) -> None:
        super().__init__()
        self.mode = mode
        self.allTags = allTags

        self.VBoxLayout = qtw.QVBoxLayout()

        self.input = qtw.QLineEdit()
        self.input.textChanged.connect(self.lineEditTextChanged)
        self.input.setPlaceholderText('To specify multiple tags seperate them with a comma ","')

        self.completer = qtw.QCompleter(self.allTags)
        self.completer.setFilterMode(qt.MatchFlag.MatchStartsWith)
        self.input.setCompleter(self.completer)

        self.buttons = qtw.QDialogButtonBox.StandardButton.Ok | qtw.QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = qtw.QDialogButtonBox(self.buttons)
        self.buttonBox.buttons()[0].setEnabled(False)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        if mode == 0:
            self.removeMode()
        else:
            self.addMode()
 
        for widget in (self.input, self.buttonBox):
            self.VBoxLayout.addWidget(widget)

        self.setLayout(self.VBoxLayout)

    def addMode(self) -> None:
        self.setWindowTitle('Add tag to mod')


    def removeMode(self) -> None:
        self.setWindowTitle('Remove tag from mod')

    
    def lineEditTextChanged(self) -> None:
        okButton = self.buttonBox.buttons()[0]

        if not len(self.input.text()) <= 0:
            okButton.setEnabled(True)
        else:
            okButton.setEnabled(False)