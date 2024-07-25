import os

from PySide6.QtCore import QCoreApplication as qapp, Slot
import PySide6.QtWidgets as qtw

from src.widgets.QDialog.QDialog import Dialog
from src.save import OptionsManager
from src.constant_vars import OPTIONS_CONFIG

class GamePathNotFound(Dialog):
    def __init__(self, QParent: qtw.QWidget | qtw.QApplication, optionsPath: str = OPTIONS_CONFIG) -> None:
        super().__init__()

        self.QParent = QParent

        style = self.style()

        self.setWindowTitle(qapp.translate('GamePathNotFound', 'Set game path'))

        self.optionsManager = OptionsManager(optionsPath)

        layout = qtw.QVBoxLayout()

        self.noticeLabel = qtw.QLabel(self)

        self.inputFrame = qtw.QFrame(self)
        inputFrameLayout = qtw.QHBoxLayout()

        self.openExplorerButton = qtw.QPushButton(icon=style.standardIcon(style.StandardPixmap.SP_DirLinkIcon), parent=self.inputFrame)
        self.openExplorerButton.setSizePolicy(qtw.QSizePolicy.Policy.Fixed, qtw.QSizePolicy.Policy.Fixed)
        self.openExplorerButton.clicked.connect(self.openFileDialog)

        self.gameDir = qtw.QLineEdit(self.inputFrame)
        self.gameDir.setPlaceholderText(qapp.translate('GamePathNotFound', 'PAYDAY 2 Game Directory'))
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

    @Slot()
    def openFileDialog(self) -> None:
        dialog = qtw.QFileDialog()
        url = dialog.getExistingDirectory(
            self,
            caption=qapp.translate('GamePathNotFound', 'Select PAYDAY 2 Directory')
        )

        if os.path.isdir(url):
            self.gameDir.setText(url)

    @Slot()
    def checkGamePath(self) -> None:

        gamePath = self.gameDir.text()
        okButton = self.buttonBox.button(qtw.QDialogButtonBox.StandardButton.Ok)

        if len(gamePath) > 0:

            okButton.setEnabled(True)

        else:

            okButton.setEnabled(False)
    
    @Slot()
    def accept(self) -> None:
        self.optionsManager.setGamepath(self.gameDir.text())
        self.optionsManager.writeData()
        return super().accept()

    @Slot()
    def reject(self) -> None:

        if isinstance(self.QParent, qtw.QApplication):
            self.QParent.shutdown()
        else:
            return super().reject()
