import logging

import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
from PySide6.QtCore import Qt as qt
from PySide6.QtNetwork import QNetworkReply

from semantic_version import Version

from src.widgets.QDialog.QDialog import Dialog
from src.constant_vars import VERSION
from src.widgets.QDialog.announcementQDialog import Notice
from src.save import OptionsManager
from src.errorChecking import openWebPage

from src.api.update import Update

class updateDetected(Dialog):

    succeededState = False
    downloadState = False
    lastIterBytes = 0

    def __init__(self, newVersion: Version, releaseNotes: str) -> None:
        super().__init__()

        self.setWindowTitle('Update Notice')
        
        self.setMinimumSize(450, 450)

        layout = qtw.QVBoxLayout()

        self.autoUpdate = Update()

        self.progressBar = qtw.QProgressBar()
        self.progressBar.setAlignment(qt.AlignmentFlag.AlignTop)

        self.autoUpdate.setTotalProgress.connect(lambda x: self.progressBar.setMaximum(x))
        self.autoUpdate.setCurrentProgress.connect(lambda x, y: self.updateProgressBar(x, y))
        self.autoUpdate.downloading.connect(lambda x, y: self.downloadStarted(x, y))
        self.autoUpdate.addTotalProgress.connect(lambda x: self.progressBar.setMaximum(self.progressBar.maximum() + x))
        self.autoUpdate.error.connect(lambda x: self.errorRaised(x))
        self.autoUpdate.succeeded.connect(self.succeeded)
        self.autoUpdate.doneCanceling.connect(self.close)

        self.message = qtw.QLabel(self, text=f'New update found: {newVersion}\nCurrent Version: {VERSION}\nDo you want to Update?')

        self.changelog = qtw.QTextBrowser(self)
        self.changelog.setMarkdown(releaseNotes)
        self.changelog.setOpenExternalLinks(True)

        self.viewWeb = qtw.QPushButton(text='View Release Notes on github.com', parent=self)
        self.viewWeb.clicked.connect(lambda: openWebPage('https://github.com/Wolfmyths/Myth-Mod-Manager/releases/latest'))

        self.buttons = qtw.QDialogButtonBox.StandardButton.Ok | qtw.QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = qtw.QDialogButtonBox(self.buttons)
        self.buttonBox.addButton('Do not ask again', qtw.QDialogButtonBox.ButtonRole.ActionRole)
        self.buttonBox.buttons()[2].clicked.connect(self.doNotAskAgain)
        self.buttonBox.accepted.connect(self.okButton)
        self.buttonBox.rejected.connect(self.cancel)

        for widget in (self.message, self.progressBar, self.changelog, self.viewWeb, self.buttonBox):
            layout.addWidget(widget)
        
        self.setLayout(layout)

    def okButton(self):

        if self.succeededState:

            self.accept()

        else:

            self.changelog.hide()
            self.buttonBox.buttons()[0].setEnabled(False)

            self.progressBar.show()

            self.autoUpdate.start()
    
    def errorRaised(self, message: str):
        error = Notice(message, headline='Error')
        error.exec()

        self.cancel()
        self.reject()

    def succeeded(self):

        self.progressBar.hide()

        self.progressBar.setValue(self.progressBar.maximum())
        self.message.setText('Installed!\nClick ok to exit and update Myth Mod Manager')

        self.succeededState = True
        self.buttonBox.buttons()[0].setEnabled(True)
    
    def cancel(self):
        '''
        Sets the cancel flag to true in which Update() will exit the function
        '''

        # Hidden implies that the download hasn't started
        if self.progressBar.isHidden():
            self.reject()

        logging.info('Task %s was canceled...')
        self.message.setText('Canceling... (Finishing current step)')

        self.autoUpdate.cancel = True
    
    def doNotAskAgain(self) -> None:
        logging.info('Do not alert me to updates button was pressed')
        options = OptionsManager()
        options.setMMMUpdateAlert(False)
        options.writeData()
        self.cancel()
    
    def downloadStarted(self, current: int, total: int) -> None:

        if self.autoUpdate.cancel:
            reply: QNetworkReply = self.autoUpdate.network.sender()
            reply.abort()
            self.reject()

        if not self.downloadState:
            self.progressBar.setMaximum(self.progressBar.maximum() + total)
            self.downloadState = True
            
        self.updateProgressBar(current - self.lastIterBytes)

        self.lastIterBytes = current
        
    
    def updateProgressBar(self, value: int, step: str = '') -> None:

        newValue = value + self.progressBar.value()

        if step:
            self.message.setText(step)

        self.progressBar.setValue(newValue)

# EVENT OVERRIDES 
    def closeEvent(self, arg__1: qtg.QCloseEvent) -> None:

        if not self.succeededState:
            self.setResult(0)
            return super().closeEvent(arg__1)
        else:
            self.accept()
    
    def exec(self) -> int:
        # Hide progress widget until it get activated
        self.progressBar.hide()
        return super().exec()
    
    def accept(self) -> None:

        self.setResult(1)

        return super().accept()