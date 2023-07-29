
import PySide6.QtWidgets as qtw

class Notice(qtw.QDialog):
    def __init__(self, message: str, headline: str = 'Notice') -> None:
        super().__init__()

        self.setWindowTitle(headline)

        layout = qtw.QVBoxLayout()

        warningLabel = qtw.QLabel(self, text=message)

        buttons = qtw.QDialogButtonBox.Ok | qtw.QDialogButtonBox.Cancel

        self.buttonBox = qtw.QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(lambda: self.accept())
        self.buttonBox.rejected.connect(lambda: self.reject())

        for widget in (warningLabel, self.buttonBox):
            layout.addWidget(widget)
        
        self.setLayout(layout)