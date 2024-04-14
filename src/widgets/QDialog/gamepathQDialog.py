import os
import sys

import PySide6.QtWidgets as qtw

from src.widgets.QDialog.QDialog import Dialog
from src.save import OptionsManager
from src.constant_vars import OPTIONS_CONFIG

class GamePathNotFound(Dialog):
    def __init__(self, QParent: qtw.QWidget | qtw.QApplication, optionsPath: str = OPTIONS_CONFIG) -> None:
        super().__init__()

        self.QParent = QParent

        style = self.style()

        self.setWindowTitle('Set gamepath')

        self.optionsManager = OptionsManager(optionsPath)

        layout = qtw.QVBoxLayout()

        self.noticeLabel = qtw.QLabel(self)

        self.inputFrame = qtw.QFrame(self)
        inputFrameLayout = qtw.QHBoxLayout()

        self.openExplorerButton = qtw.QPushButton(icon=style.standardIcon(style.StandardPixmap.SP_DirLinkIcon), parent=self.inputFrame)
        self.openExplorerButton.setSizePolicy(qtw.QSizePolicy.Policy.Fixed, qtw.QSizePolicy.Policy.Fixed)
        self.openExplorerButton.clicked.connect(self.openFileDialog)

        self.gameDir = qtw.QLineEdit(self.inputFrame)
        self.gameDir.setPlaceholderText('PAYDAY 2 Game Directory')
        self.gameDir.textChanged.connect(self.checkGamePath)

        for widget in (self.gameDir, self.openExplorerButton):
            inputFrameLayout.addWidget(widget)

        self.inputFrame.setLayout(inputFrameLayout)

        buttons = qtw.QDialogButtonBox.StandardButton.Ok | qtw.QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = qtw.QDialogButtonBox(buttons)
        self.buttonBox.button(qtw.QDialogButtonBox.StandardButton.Ok).setEnabled(False)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        for widget in (self.noticeLabel, self.inputFrame, self.buttonBox):
            layout.addWidget(widget)

        self.setLayout(layout)

    def openFileDialog(self) -> None:
        dialog = qtw.QFileDialog()
        url = dialog.getExistingDirectory(self, caption='Select PAYDAY 2 Directory')

        if os.path.isdir(url):
            self.gameDir.setText(url)

    def checkGamePath(self) -> None:

        gamePath = self.gameDir.text()
        okButton = self.buttonBox.button(qtw.QDialogButtonBox.StandardButton.Ok)

        if len(gamePath) > 0:

            okButton.setEnabled(True)

        else:

            okButton.setEnabled(False)
    
    def accept(self) -> None:
        self.optionsManager.setGamepath(self.gameDir.text())
        self.optionsManager.writeData()
        return super().accept()

    def reject(self) -> None:

        if isinstance(self.QParent, qtw.QApplication):
            self.QParent.shutdown()
        else:
            return super().reject()
