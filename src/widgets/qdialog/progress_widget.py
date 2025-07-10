from __future__ import annotations
from typing import TYPE_CHECKING

import logging

import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw
from PySide6.QtCore import (
    QThread, QCoreApplication as qapp, Slot, QMutex, QMutexLocker, QSignalBlocker
)

from src.widgets.qdialog.QDialog import Dialog

if TYPE_CHECKING:
    from src.objects.worker import Worker

class ProgressWidget(Dialog):
    '''
    QDialog object to show the progress of threaded functions
    '''

    def __init__(self, mode: Worker) -> None:
        super().__init__()
        logging.getLogger(__name__)

        self.setWindowTitle(qapp.translate('ProgressWidget', 'Myth Mod Manager Task'))

        self.mutex = QMutex()

        self.mode: Worker = mode
        self.mode.mutex = self.mutex

        layout = qtw.QVBoxLayout()

        # Label
        self.infoLabel = qtw.QLabel(self)

        # Progress bar
        self.progressBar = qtw.QProgressBar(self)

        # Button
        buttons = qtw.QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = qtw.QDialogButtonBox(buttons)
        self.buttonBox.rejected.connect(self.cancel)

        for widget in (self.infoLabel, self.progressBar, self.buttonBox):
            layout.addWidget(widget)
        
        self.setLayout(layout)

        self.__initMode()

    def __initMode(self) -> None:
        # Create QThread
        self.qthread = QThread(self)

        # Move task to QThread
        self.mode.moveToThread(self.qthread)
        
        # Connect signals
        self.qthread.started.connect(self.mode.start)
        self.mode.setTotalProgress.connect(self.setMaxProgress)
        self.mode.setCurrentProgress.connect(self.updateProgressBar)
        self.mode.addTotalProgress.connect(self.addMaxProgress)
        self.mode.doneCanceling.connect(self.reject)
        self.mode.error.connect(self.errorRaised)
        self.mode.succeeded.connect(self.succeeded)
    
    def exec(self) -> int:

        self.qthread.start()
        return super().exec()

    @Slot(str)
    def errorRaised(self, message: str) -> None:
        logging.error(message)
        with QSignalBlocker(self.infoLabel):
            self.infoLabel.setText(
                f'{message}\n'+
                qapp.translate('ProgressWidget', 'Exit to continue')
            )
        self.cleanup()

    @Slot()
    def succeeded(self) -> None:
        with QSignalBlocker(self.infoLabel):
            self.infoLabel.setText(qapp.translate('ProgressWidget', 'Done!'))

        with QSignalBlocker(self.progressBar):
            self.progressBar.setValue(self.progressBar.maximum())

        self.accept()
    
    def cleanup(self) -> None:
        self.qthread.quit()
        self.qthread.wait()
        self.mode.deleteLater()

    def closeEvent(self, arg__1: qtg.QCloseEvent) -> None:
        if self.qthread.isRunning():
            self.cancel()
        else:
            self.cleanup()
            return super().closeEvent(arg__1)
    
    @Slot()
    def reject(self) -> None:
        self.cleanup()
        return super().reject()
    
    @Slot()
    def accept(self) -> None:
        self.cleanup()
        return super().accept()

    @Slot()
    def cancel(self) -> None:
        '''
        Sets the cancel flag to true in Worker and disables the cancel button
        '''

        logging.info('Task %s was canceled', str(self.mode))
        with QSignalBlocker(self.infoLabel):
            self.infoLabel.setText(qapp.translate('ProgressWidget', 'Canceled'))

        with QMutexLocker(self.mutex):
            self.mode.cancel = True
        button: qtw.QPushButton = self.buttonBox.button(qtw.QDialogButtonBox.StandardButton.Cancel)
        with QSignalBlocker(button):
            button.setDisabled(True)

    @Slot(int)
    def addMaxProgress(self, x: int) -> None:
        with QSignalBlocker(self.progressBar):
            max: int = self.progressBar.maximum()
            self.progressBar.setMaximum(max + x)

    @Slot(int)
    def setMaxProgress(self, x: int) -> None:
        with QSignalBlocker(self.progressBar):
            self.progressBar.setMaximum(x)

    @Slot(int, str)
    def updateProgressBar(self, x: int, y: str) -> None:
        '''
        Adds progress to the current progress
        bar value and changes the text of the label
        '''
        #with QSignalBlocker(self.infoLabel):
        self.infoLabel.setText(y)
        #with QSignalBlocker(self.progressBar):
        newValue: int = x + self.progressBar.value()
        self.progressBar.setValue(newValue)
