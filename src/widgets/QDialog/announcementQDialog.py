import PySide6.QtWidgets as qtw

from src.widgets.QDialog.QDialog import Dialog

class Notice(Dialog):
    def __init__(self, message: str, headline: str = 'Notice') -> None:
        super().__init__()

        self.setWindowTitle(headline)

        layout = qtw.QVBoxLayout()

        self.warningLabel = qtw.QLabel(self, text=message)
        self.warningLabel.setWordWrap(True)

        buttons = qtw.QDialogButtonBox.StandardButton.Ok

        self.buttonBox = qtw.QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)

        for widget in (self.warningLabel, self.buttonBox):
            layout.addWidget(widget)
        
        self.setLayout(layout)