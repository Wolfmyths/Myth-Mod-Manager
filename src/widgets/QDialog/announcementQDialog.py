
import PySide6.QtWidgets as qtw

from widgets.QDialog.QDialog import Dialog

class Notice(Dialog):
    def __init__(self, message: str, headline: str = 'Notice') -> None:
        super().__init__()

        self.setWindowTitle(headline)

        layout = qtw.QVBoxLayout()

        warningLabel = qtw.QLabel(self, text=message)
        warningLabel.setWordWrap(True)

        buttons = qtw.QDialogButtonBox.Ok

        self.buttonBox = qtw.QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(lambda: self.accept())

        for widget in (warningLabel, self.buttonBox):
            layout.addWidget(widget)
        
        self.setLayout(layout)