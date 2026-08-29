import PySide6.QtWidgets as qtw
from PySide6.QtCore import QCoreApplication as qapp, Slot
from typing_extensions import override

from src.widgets.qdialog.dialog import Dialog

class InsertString(Dialog):
    '''QDialog class that requests a string input from the user'''

    userInput: str | None = None

    def __init__(self, prompt: str) -> None:
        super().__init__()

        layout = qtw.QVBoxLayout()

        self.setWindowTitle(qapp.translate('insertString', 'Insert text'))

        self.label = qtw.QLabel(prompt, self)

        self.inputString = qtw.QLineEdit(parent=self)

        buttons = qtw.QDialogButtonBox.StandardButton.Ok | qtw.QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = qtw.QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        for widget in (self.label, self.inputString, self.buttonBox):
            layout.addWidget(widget)
        
        self.setLayout(layout)

    @override
    @Slot()
    def accept(self) -> None:

        self.userInput = self.inputString.text()

        self.setResult(1)

        return super().accept()

    @override
    @Slot()
    def reject(self) -> None:
        self.setResult(0)
        return super().reject()