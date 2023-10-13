import PySide6.QtWidgets as qtw

from src.widgets.QDialog.QDialog import Dialog

class insertString(Dialog):
    '''QDialog class that requests a string input from the user'''

    userInput: str | None = None

    def __init__(self, prompt: str) -> None:
        super().__init__()

        layout = qtw.QVBoxLayout()

        self.setWindowTitle('Insert text')

        self.label = qtw.QLabel(prompt, self)

        self.inputString = qtw.QLineEdit(parent=self)

        buttons = qtw.QDialogButtonBox.StandardButton.Ok | qtw.QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = qtw.QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(lambda: self.accept())
        self.buttonBox.rejected.connect(lambda: self.reject())

        for widget in (self.label, self.inputString, self.buttonBox):
            layout.addWidget(widget)
        
        self.setLayout(layout)

    def accept(self) -> None:

        self.userInput = self.inputString.text()

        self.setResult(1)

        return super().accept()
    
    def reject(self) -> None:
        self.setResult(0)
        return super().reject()