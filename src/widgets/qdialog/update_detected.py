import logging

import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
from PySide6.QtCore import Qt as qt, QCoreApplication as qapp, Slot

from semantic_version import Version

from src.widgets.qdialog.QDialog import Dialog
from src.constant_vars import VERSION
from src.widgets.qdialog.notice import Notice
from src.helpers.options_manager import OptionsManager
from src.helpers.helper import openWebPage

from src.api.update import Update

class UpdateDetected(Dialog):

    succeededState = False
    downloadState = False
    lastIterBytes = 0

    def __init__(self, newVersion: Version, releaseNotes: str) -> None:
        super().__init__()

        self.setWindowTitle(qapp.translate('updateDetected', 'Update Notice'))
        
        self.setMinimumSize(450, 450)

        layout = qtw.QVBoxLayout()

        self.autoUpdate = Update()

        self.progressBar = qtw.QProgressBar(self)
        self.progressBar.setAlignment(qt.AlignmentFlag.AlignTop)

        self.autoUpdate.setTotalProgress.connect(self.onSetTotalProgress)
        self.autoUpdate.setCurrentProgress.connect(self.updateProgressBar)
        self.autoUpdate.downloadProgressUpdated.connect(self.onDownloadProgress)
        self.autoUpdate.addTotalProgress.connect(self.onAddTotalProgress)
        self.autoUpdate.error.connect(self.errorRaised)
        self.autoUpdate.succeeded.connect(self.succeeded)
        self.autoUpdate.doneCanceling.connect(self.close)

        self.message = qtw.QLabel(
            self,
            text=qapp.translate('updateDetected', 'New update found:') +
                f' {newVersion}\n' +
                qapp.translate('updateDetected', 'Current Version:') +
                f' {VERSION}\n' +
                qapp.translate('updateDetected', 'Do you want to Update?')
        )

        self.changelog = qtw.QTextBrowser(self)
        self.changelog.setMarkdown(releaseNotes)
        self.changelog.setOpenExternalLinks(True)

        self.viewWeb = qtw.QPushButton(text=qapp.translate('updateDetected', 'View Release Notes on github.com'), parent=self)
        self.viewWeb.clicked.connect(lambda: openWebPage('https://github.com/Wolfmyths/Myth-Mod-Manager/releases/latest'))

        self.buttons = qtw.QDialogButtonBox.StandardButton.Ok | qtw.QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = qtw.QDialogButtonBox(self.buttons)
        self.buttonBox.addButton(qapp.translate('updateDetected', 'Do not ask again'), qtw.QDialogButtonBox.ButtonRole.ActionRole)
        self.buttonBox.buttons()[2].clicked.connect(self.doNotAskAgain)
        self.buttonBox.accepted.connect(self.okButton)
        self.buttonBox.rejected.connect(self.cancel)

        for widget in (self.message, self.progressBar, self.changelog, self.viewWeb, self.buttonBox):
            layout.addWidget(widget)
        
        self.setLayout(layout)

    @Slot()
    def okButton(self) -> None:

        if self.succeededState:

            self.accept()

        else:

            self.changelog.hide()
            self.buttonBox.buttons()[0].setEnabled(False)

            self.progressBar.show()

            self.autoUpdate.start()
    
    @Slot(str)
    def errorRaised(self, message: str) -> None:
        logging.error(message)
        error = Notice(message, headline=qapp.translate('updateDetected', 'Error'))
        error.exec()

        self.cancel()
        self.reject()

    @Slot()
    def succeeded(self) -> None:

        self.progressBar.hide()

        self.progressBar.setValue(self.progressBar.maximum())
        self.message.setText(
            qapp.translate('updateDetected', 'Installation Successful!') +
            '\n' +
            qapp.translate('updateDetected', 'Click ok to exit and update Myth Mod Manager')
        )

        self.succeededState = True
        self.buttonBox.buttons()[0].setEnabled(True)
    
    @Slot(int)
    def onSetTotalProgress(self, newMax: int) -> None:
        self.progressBar.setMaximum(newMax)
    
    @Slot(int)
    def onAddTotalProgress(self, num: int) -> None:
        self.progressBar.setMaximum(self.progressBar.maximum() + num)

    @Slot()
    def cancel(self) -> None:
        '''
        Sets the cancel flag to true in which Update() will exit the function
        '''

        # Hidden implies that the download hasn't started
        if self.progressBar.isHidden():
            self.reject()

        logging.info('Task %s was canceled...')
        self.message.setText(qapp.translate('updateDetected', 'Canceling... (Finishing current step)'))

        self.autoUpdate.abort()
    
    @Slot()
    def doNotAskAgain(self) -> None:
        logging.info('Do not alert me to updates button was pressed')
        options = OptionsManager()
        options.setMMMUpdateAlert(False)
        options.writeData()
        self.cancel()
    
    @Slot(int, int)
    def onDownloadProgress(self, current: int, total: int) -> None:

        if self.autoUpdate.cancel:
            return

        #logging.info("Bytes Recieved: %s", current)

        # First time being updated
        if not self.downloadState:
            #logging.info("TOTAL BYTES: %s", total)
            self.progressBar.setMaximum(total)
            self.downloadState = True
        
        self.progressBar.setValue(current)
        
    @Slot(int)
    @Slot(int, str)
    def updateProgressBar(self, value: int, step: str = '') -> None:

        if step:
            self.message.setText(step)
    
        newValue: int = value + self.progressBar.value()
        self.progressBar.setValue(newValue)

# EVENT OVERRIDES 
    def closeEvent(self, arg__1: qtg.QCloseEvent) -> None:

        if not self.succeededState:
            self.setResult(qtw.QDialog.DialogCode.Rejected)
            return super().closeEvent(arg__1)
        else:
            self.accept()
    
    def exec(self) -> int:
        # Hide progress widget until it get activated
        self.progressBar.hide()
        return super().exec()
    
    def accept(self) -> None:

        self.setResult(qtw.QDialog.DialogCode.Accepted)

        return super().accept()