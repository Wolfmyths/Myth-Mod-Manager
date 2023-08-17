
import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
from PySide6.QtCore import Qt as qt

from constant_vars import ICON

class Notice(qtw.QDialog):
    def __init__(self, message: str, headline: str = 'Notice') -> None:
        super().__init__()

        self.setWindowTitle(headline)
        self.setWindowIcon(qtg.QIcon(ICON))
        self.setWindowFlag(qt.WindowType.WindowStaysOnTopHint, True)

        layout = qtw.QVBoxLayout()

        warningLabel = qtw.QLabel(self, text=message)
        warningLabel.setWordWrap(True)

        buttons = qtw.QDialogButtonBox.Ok

        self.buttonBox = qtw.QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(lambda: self.accept())

        for widget in (warningLabel, self.buttonBox):
            layout.addWidget(widget)
        
        self.setLayout(layout)