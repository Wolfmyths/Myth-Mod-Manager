
import os

import PySide6.QtWidgets as qtw

from src.widgets.QDialog.QDialog import Dialog
from src.save import OptionsManager
from src.constant_vars import OPTIONS_CONFIG

class GamePathNotFound(Dialog):
    def __init__(self, QParent: qtw.QWidget | qtw.QApplication, optionsPath: str = OPTIONS_CONFIG) -> None:
        super().__init__()

        self.QParent = QParent

        self.setWindowTitle('Gamepath Not Found')

        self.optionsManager = OptionsManager(optionsPath)

        layout = qtw.QFormLayout()
        layout.setRowWrapPolicy(qtw.QFormLayout.RowWrapPolicy.WrapAllRows)

        self.noticeLabel = qtw.QLabel(self)
        self.noticeLabelDesc = qtw.QLabel(self)

        self.gameDirLabel = qtw.QLabel(self, text='Payday 2 Game Path:')

        self.gameDir = qtw.QLineEdit(self)
        self.gameDir.setText(self.optionsManager.getGamepath())
        self.gameDir.textChanged.connect(self.checkGamePath)

        buttons = qtw.QDialogButtonBox.StandardButton.Ok | qtw.QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = qtw.QDialogButtonBox(buttons)
        self.buttonBox.button(qtw.QDialogButtonBox.StandardButton.Ok).setEnabled(False)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        for row in ( (self.noticeLabel, self.noticeLabelDesc),
                     (self.gameDirLabel, self.gameDir),
                     (qtw.QLabel(), self.buttonBox)):

            layout.addRow(row[0], row[1])
        
        self.setLayout(layout)
    
    def checkGamePath(self):

        gamePath = self.gameDir.text()
        okButton = self.buttonBox.button(qtw.QDialogButtonBox.StandardButton.Ok)

        if os.path.isfile(os.path.join(gamePath, 'payday2_win32_release.exe')):

            okButton.setEnabled(True)

            self.noticeLabel.setText('Success:')
            self.noticeLabelDesc.setText('Game Path is valid')

            self.optionsManager.setGamepath(gamePath)

        else:

            okButton.setEnabled(False)

            self.noticeLabel.setText('Error:')
            self.noticeLabelDesc.setText('Game Path is not valid')

    def reject(self) -> None:

        if type(self.QParent) is qtw.QApplication:
            self.QParent.shutdown()
        return super().reject()
