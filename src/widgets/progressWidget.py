import logging

import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw

from src.widgets.QDialog.QDialog import Dialog

from src.threaded.file_mover import FileMover

class ProgressWidget(Dialog):
    '''
    QDialog object to show the progress of threaded functions
    '''

    def __init__(self, mode: FileMover) -> None:
        super().__init__()

        self.mode = mode

        logging.getLogger(__name__)

        self.setWindowTitle('Myth Mod Manager Task')

        layout = qtw.QVBoxLayout()

        self.warningLabel = qtw.QLabel(self)

        self.progressBar = qtw.QProgressBar()
        self.mode.setTotalProgress.connect(lambda x: self.progressBar.setMaximum(x))
        self.mode.setCurrentProgress.connect(lambda x, y: self.updateProgressBar(x, y))
        self.mode.addTotalProgress.connect(lambda x: self.progressBar.setMaximum(self.progressBar.maximum() + x))
        self.mode.error.connect(lambda x: self.errorRaised(x))

        self.mode.succeeded.connect(lambda: self.succeeded())

        buttons = qtw.QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = qtw.QDialogButtonBox(buttons)
        self.buttonBox.rejected.connect(lambda: self.cancel())

        for widget in (self.warningLabel, self.progressBar, self.buttonBox):
            layout.addWidget(widget)
        
        self.setLayout(layout)
    
    def exec(self) -> int:

        self.mode.start()
        return super().exec()
    
    def errorRaised(self, message: str):
        self.warningLabel.setText(message)

    def succeeded(self):
        self.progressBar.setValue(self.progressBar.maximum())
        self.warningLabel.setText('Done!')

        self.mode.terminate()
        self.mode.deleteLater()

        self.accept()
    
    def closeEvent(self, arg__1: qtg.QCloseEvent) -> None:

        if self.mode.isRunning():
            self.cancel()
        else:
            return super().closeEvent(arg__1)
    
    def cancel(self):
        '''
        Sets the cancel flag to true in which FileMover() will exit the function
        after it's done a step and pass the success signal
        '''

        isModeCanceled = self.mode.cancel

        if isModeCanceled:
            self.reject()

        logging.info('Task %s was canceled...', str(self.mode))
        self.warningLabel.setText('Canceling... (Finishing current step)')

        isModeCanceled = True
    
    def updateProgressBar(self, x, y):

        newValue = x + self.progressBar.value()

        self.warningLabel.setText(y)
        self.progressBar.setValue(newValue)
