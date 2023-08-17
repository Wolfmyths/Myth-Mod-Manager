
import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
from PySide6.QtCore import Qt as qt

from constant_vars import ICON

class DeleteModConfirmation(qtw.QDialog):
    def __init__(self, QParent: qtw.QWidget | qtw.QApplication) -> None:
        super().__init__()

        self.QParent = QParent
        self.setWindowTitle('Mods are about to be permanently deleted!')
        self.setWindowFlag(qt.WindowType.WindowStaysOnTopHint)
        self.setWindowIcon(qtg.QIcon(ICON))

        layout = qtw.QVBoxLayout()

        warningLabel = qtw.QLabel(self, text='Are you sure you want to delete these mod(s) from your computer?\n(This action cannot be reversed)')

        buttons = qtw.QDialogButtonBox.Ok | qtw.QDialogButtonBox.Cancel

        self.buttonBox = qtw.QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(lambda: self.accept())
        self.buttonBox.rejected.connect(lambda: self.reject())

        for widget in (warningLabel, self.buttonBox):
            layout.addWidget(widget)
        
        self.setLayout(layout)
    
    def accept(self) -> None:
        self.setResult(1)
        return super().accept()
    
    def reject(self) -> None:
        self.setResult(0)
        return super().reject()