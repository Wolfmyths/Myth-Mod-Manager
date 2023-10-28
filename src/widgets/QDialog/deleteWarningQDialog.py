
import PySide6.QtWidgets as qtw

from src.widgets.QDialog.QDialog import Dialog

class DeleteModConfirmation(Dialog):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle('Mods are about to be permanently deleted!')

        layout = qtw.QVBoxLayout()

        warningLabel = qtw.QLabel(self, text='Are you sure you want to delete these mod(s) from your computer?\n(This action cannot be reversed)')

        buttons = qtw.QDialogButtonBox.StandardButton.Ok | qtw.QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = qtw.QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        for widget in (warningLabel, self.buttonBox):
            layout.addWidget(widget)
        
        self.setLayout(layout)
    
    def accept(self) -> None:
        self.setResult(1)
        return super().accept()
    
    def reject(self) -> None:
        self.setResult(0)
        return super().reject()