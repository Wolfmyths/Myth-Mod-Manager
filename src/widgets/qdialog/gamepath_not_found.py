from PySide6.QtCore import QCoreApplication as qapp, Slot, QFileInfo
import PySide6.QtWidgets as qtw

from typing_extensions import override

from src.widgets.qdialog.dialog import Dialog
from src.helpers.options_manager import OptionsManager

class GamePathNotFound(Dialog):
    def __init__(self, parent: qtw.QWidget | None = None) -> None:
        super().__init__(parent=parent)

        style: qtw.QStyle = self.style()

        self.setWindowTitle(qapp.translate('GamePathNotFound', 'Set game path'))

        layout = qtw.QVBoxLayout()

        self.noticeLabel = qtw.QLabel(self)

        self.inputFrame = qtw.QFrame(self)
        inputFrameLayout = qtw.QHBoxLayout()

        self.openExplorerButton = qtw.QPushButton(style.standardIcon(style.StandardPixmap.SP_DirLinkIcon), '', parent=self.inputFrame)
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
        url: str = qtw.QFileDialog.getOpenFileUrl(
            self,
            caption=qapp.translate('GamePathNotFound', 'Select PAYDAY 2 Executable')
        )[1]

        if QFileInfo(url).isExecutable():
            self.gameDir.setText(url)

    @Slot()
    def checkGamePath(self) -> None:

        gamePath: str = self.gameDir.text()
        okButton: qtw.QPushButton = self.buttonBox.button(qtw.QDialogButtonBox.StandardButton.Ok)

        okButton.setEnabled(len(gamePath) > 0)
    
    @override
    @Slot()
    def accept(self) -> None:
        OptionsManager.setGameExecuteable(self.gameDir.text())
        OptionsManager.writeData()
        return super().accept()

    @override
    @Slot()
    def reject(self) -> None:
        qapp.instance().shutdown()
        return super().reject()
