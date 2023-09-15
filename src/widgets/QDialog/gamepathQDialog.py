
import os

import PySide6.QtWidgets as qtw
from PySide6.QtCore import QTimer

from widgets.QDialog.QDialog import Dialog
from save import OptionsManager
from constant_vars import OPTIONS_SECTION, OPTIONS_GAMEPATH

class GamePathNotFound(Dialog):
    def __init__(self, QParent: qtw.QWidget | qtw.QApplication) -> None:
        super().__init__()

        self.QParent = QParent

        self.setWindowTitle('Gamepath Not Found')

        self.optionsManager = OptionsManager()

        self.timeout = QTimer()
        self.timeout.timeout.connect(lambda: self.setGamePathTimeout())

        layout = qtw.QFormLayout()
        layout.setRowWrapPolicy(qtw.QFormLayout.RowWrapPolicy.WrapAllRows)

        self.noticeLabel = qtw.QLabel(self)
        self.noticeLabelDesc = qtw.QLabel(self)

        self.gameDirLabel = qtw.QLabel(self, text='Payday 2 Game Path:')

        self.gameDir = qtw.QLineEdit(self)
        self.gameDir.setText(self.optionsManager.getOption(OPTIONS_GAMEPATH))
        self.gameDir.textChanged.connect(lambda: self.setGamePath())

        buttons = qtw.QDialogButtonBox.Ok | qtw.QDialogButtonBox.Cancel

        self.buttonBox = qtw.QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(lambda: self.accept())
        self.buttonBox.rejected.connect(lambda: self.reject())

        for row in ( (self.noticeLabel, self.noticeLabelDesc),
                     (self.gameDirLabel, self.gameDir),
                     (qtw.QLabel(), self.buttonBox)):

            layout.addRow(row[0], row[1])
        
        self.setLayout(layout)
    
    def setGamePath(self):
        '''
        QTimer is started so the save data function isn't called everytime the user changes a single character

        setGamePathTimeout() is the function that actually saves the gamePath
        '''

        self.noticeLabelDesc.setText('Validating Game Path...')

        if not self.timeout.isActive():

            self.timeout.start(1000)

        else:

            self.timeout.stop()
            self.timeout.start(1000)
    
    def setGamePathTimeout(self):

        self.timeout.stop()

        gamePath = self.gameDir.text()

        if os.path.exists(os.path.join(gamePath, 'payday2_win32_release.exe')):

            self.noticeLabel.setText('Success:')
            self.noticeLabelDesc.setText('Game Path is valid')

            self.optionsManager.setOption(gamePath, OPTIONS_GAMEPATH)

        else:

            self.noticeLabel.setText('Error:')
            self.noticeLabelDesc.setText('Game Path is not valid')
    
    def reject(self) -> None:

        if type(self.QParent) == qtw.QApplication:
            self.QParent.shutdown()

        return super().reject()
        