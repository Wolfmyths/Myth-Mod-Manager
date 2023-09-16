
import webbrowser
import logging

import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg

from semantic_version import Version

from widgets.QDialog.QDialog import Dialog
from constant_vars import VERSION
from widgets.QDialog.announcementQDialog import Notice

from update import Update

class updateDetected(Dialog):

    cancelState = False
    succeededState = False

    def __init__(self, newVersion: Version, releaseNotes: str) -> None:
        super().__init__()

        self.setWindowTitle('Update Notice')
        
        self.setMinimumSize(450, 450)

        layout = qtw.QVBoxLayout()

        self.autoUpdate = Update()

        self.progressBar = qtw.QProgressBar()
        self.autoUpdate.setTotalProgress.connect(lambda x: self.progressBar.setMaximum(x))
        self.autoUpdate.setCurrentProgress.connect(lambda x, y: self.updateProgressBar(x, y))
        self.autoUpdate.addTotalProgress.connect(lambda x: self.progressBar.setMaximum(self.progressBar.maximum() + x))

        self.message = qtw.QLabel(self, text=f'New update found: {newVersion}\nCurrent Version: {VERSION}\nDo you want to Update?')

        self.autoUpdate.succeeded.connect(lambda: self.succeeded())

        self.changelog = qtw.QTextBrowser(self)
        self.changelog.setMarkdown(releaseNotes)

        self.viewWeb = qtw.QPushButton(text='View Release Notes on github.com', parent=self)
        self.viewWeb.clicked.connect(lambda: self.openBrowser())

        self.buttons = qtw.QDialogButtonBox.Ok | qtw.QDialogButtonBox.Cancel

        self.buttonBox = qtw.QDialogButtonBox(self.buttons)
        self.buttonBox.accepted.connect(lambda: self.okButton())
        self.buttonBox.rejected.connect(lambda: self.close())

        for widget in (self.progressBar, self.message, self.changelog, self.viewWeb, self.buttonBox):
            layout.addWidget(widget)
        
        self.setLayout(layout)

    def okButton(self):

        if self.succeededState:

            self.accept()

        elif not self.autoUpdate.isRunning():

            self.changelog.hide()

            self.progressBar.show()

            self.autoUpdate.start()

        elif self.cancelState:

            self.close()
    
    def exec(self) -> int:
        # Hide progress widget until it get activated
        self.progressBar.hide()
        return super().exec()
    
    def accept(self) -> None:

        self.setResult(1)

        return super().accept()
    
    def openBrowser(self):

        try:
            webbrowser.open_new_tab('https://github.com/Wolfmyths/Myth-Mod-Manager/releases/latest')
        except Exception as e:

            logging.error('Could not open web browser:\n%s', str(e))

            notice = Notice(f'Could not connect to webpage:\n{e}', 'Error:')
            notice.exec()

    
    def errorRaised(self, message: str):
        error = Notice(message, headline='Error')
        error.exec()

        self.cancel()
        self.close()

    def succeeded(self):
        
        self.autoUpdate.terminate()

        self.progressBar.hide()

        self.progressBar.setValue(self.progressBar.maximum())
        self.message.setText('Installed!\nThe next time Myth Mod Manager starts up it will delete the old version')

        self.succeededState = True
    
    def closeEvent(self, arg__1: qtg.QCloseEvent) -> None:

        if not self.succeededState:
            self.setResult(0)
        else:
            self.accept()

        if self.autoUpdate.isRunning():
            self.cancel()
        else:
            return super().closeEvent(arg__1)
    
    def cancel(self):
        '''
        Sets the cancel flag to true in which Update() will exit the function
        '''

        logging.info('Task %s was canceled...')
        self.message.setText('Canceling... (Finishing current step)')

        self.autoUpdate.cancel = True

        self.cancelState = True
    
    def updateProgressBar(self, x, y):

        newValue = x + self.progressBar.value()

        self.message.setText(y)
        self.progressBar.setValue(newValue)