from typing import Self

import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw

from fileMover import FileMover
from widgets.announcementQDialog import Notice

class StartFileMover(qtw.QDialog):
    '''
    This is a QDialog object to show the progress of functions in FileMover()

    The parameters in this class are used to pass onto FileMover()

    Possible parameters for mode:
    
    + 0 : moveToDisabledDir(*mods: str)
    + 1 : moveToEnableModDir(*mods: str)
    + 2 : changeModType(*mods: Tuple[QUrl, str])
    + 3 : unZipMod(*mods: Tuple[QUrl, str])
    + 4 : deleteMod(*modName: str)
    + 5 : backupMods()
    '''

    def __init__(self, mode: int, *args) -> None:
        super().__init__()

        self.setWindowTitle('Update Notice')

        self.fileMover = FileMover(mode, *args)
        self.fileMover.error.connect(lambda x: self.errorRaised(x))

        self.rar = []

        layout = qtw.QVBoxLayout()

        self.warningLabel = qtw.QLabel(self)

        self.progressBar = qtw.QProgressBar()
        self.fileMover.setTotalProgress.connect(lambda x: self.progressBar.setMaximum(x))
        self.fileMover.setCurrentProgress.connect(lambda x, y: self.updateProgressBar(x, y))

        self.fileMover.succeeded.connect(lambda: self.succeeded())

        buttons = qtw.QDialogButtonBox.Cancel

        self.buttonBox = qtw.QDialogButtonBox(buttons)
        self.buttonBox.rejected.connect(lambda: self.cancel())

        for widget in (self.warningLabel, self.progressBar, self.buttonBox):
            layout.addWidget(widget)
        
        self.setLayout(layout)
    
    def exec(self) -> int:

        self.fileMover.start()
        return super().exec()
    
    def errorRaised(self, message: str):
        error = Notice(message, headline='Error')
        error.exec()

        self.cancel()

    def succeeded(self):
        self.progressBar.setValue(self.progressBar.maximum())
        self.warningLabel.setText('Done!')

        self.fileMover.terminate()
        self.fileMover.deleteLater()

        self.accept()
    
    def closeEvent(self, arg__1: qtg.QCloseEvent) -> None:

        if self.fileMover.isRunning():
            self.cancel()
        else:
            return super().closeEvent(arg__1)
    
    def cancel(self):
        '''
        Sets the cancel flag to true in which FileMover() will exit the function
        after it's done a step and pass the success signal
        '''

        self.warningLabel.setText('Canceling...')

        self.fileMover.cancel = True
    
    def updateProgressBar(self, x, y):

        newValue = x + self.progressBar.value()

        self.warningLabel.setText(y)
        self.progressBar.setValue(newValue)