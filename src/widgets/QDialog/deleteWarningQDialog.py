import PySide6.QtWidgets as qtw

from src.widgets.QDialog.QDialog import Dialog

class Confirmation(Dialog):
    def __init__(self, title: str, body: str) -> None:
        super().__init__()

        self.setWindowTitle(title)

        layout = qtw.QVBoxLayout()

        self.warningLabel = qtw.QLabel(self, text=body)

        buttons = qtw.QDialogButtonBox.StandardButton.Ok | qtw.QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = qtw.QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        for widget in (self.warningLabel, self.buttonBox):
            layout.addWidget(widget)
        
        self.setLayout(layout)
    
    def accept(self) -> None:
        self.setResult(1)
        return super().accept()
    
    def reject(self) -> None:
        self.setResult(0)
        return super().reject()