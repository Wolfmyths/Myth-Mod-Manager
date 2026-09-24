import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt as qt, QCoreApplication as qapp, Slot

from src.widgets.qdialog.dialog import Dialog

class TagHandler(Dialog):

    # Modes
    REMOVE = 0
    ADD = 1

    def __init__(self, mode: int, allTags: list[str], parent: qtw.QWidget | None = None) -> None:
        super().__init__(parent)
        self.mode: int = mode
        self.allTags: list[str] = allTags

        self.VBoxLayout = qtw.QVBoxLayout()

        self.input = qtw.QLineEdit()
        self.input.textChanged.connect(self.lineEditTextChanged)
        self.input.setPlaceholderText(qapp.translate('TagHandler', 'To specify multiple tags seperate them with a comma ","'))

        self.completer = qtw.QCompleter(self.allTags)
        self.completer.setFilterMode(qt.MatchFlag.MatchStartsWith)
        self.input.setCompleter(self.completer)

        buttons = qtw.QDialogButtonBox.StandardButton.Ok | qtw.QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = qtw.QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        okButton = self.buttonBox.button(qtw.QDialogButtonBox.StandardButton.Ok)
        okButton.setEnabled(False)

        if mode == TagHandler.REMOVE:
            self.removeMode()
        else:
            self.addMode()
 
        for widget in (self.input, self.buttonBox):
            self.VBoxLayout.addWidget(widget)

        self.setLayout(self.VBoxLayout)

    def addMode(self) -> None:
        self.setWindowTitle(qapp.translate('TagHandler', 'Add tag to mod'))

    def removeMode(self) -> None:
        self.setWindowTitle(qapp.translate('TagHandler', 'Remove tag from mod'))

    @Slot(str)
    def lineEditTextChanged(self, new_text: str) -> None:
        okButton = self.buttonBox.button(qtw.QDialogButtonBox.StandardButton.Ok)

        enabled = len(new_text) > 0
        okButton.setEnabled(enabled)