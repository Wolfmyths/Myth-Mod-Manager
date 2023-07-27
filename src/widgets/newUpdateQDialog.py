
import webbrowser
from semantic_version import Version

from constant_vars import VERSION

import PySide6.QtWidgets as qtw

class updateDetected(qtw.QDialog):
    def __init__(self, newVersion: Version) -> None:
        super().__init__()

        self.setWindowTitle('Update Notice')

        layout = qtw.QVBoxLayout()

        warningLabel = qtw.QLabel(self, text=f'New update found: {newVersion}\nCurrent Version: {VERSION}\nDo you want to Update?')

        buttons = qtw.QDialogButtonBox.Ok | qtw.QDialogButtonBox.Cancel

        self.buttonBox = qtw.QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(lambda: self.accept())
        self.buttonBox.rejected.connect(lambda: self.reject())

        for widget in (warningLabel, self.buttonBox):
            layout.addWidget(widget)
        
        self.setLayout(layout)
    
    def accept(self) -> None:

        webbrowser.open_new_tab('https://github.com/Wolfmyths/Myth-Mod-Manager/releases/latest')

        self.setResult(1)

        return super().accept()