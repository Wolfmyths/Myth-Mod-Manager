import os
import logging

import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt as qt, Signal

from src.widgets.QDialog.announcementQDialog import Notice
from src.widgets.QDialog.deleteWarningQDialog import DeleteModConfirmation

from src import errorChecking

class ExternalTool(qtw.QFrame):
    deleted = Signal(str)
    nameChanged = Signal(str, str)
    def __init__(self, toolURL: str) -> None:
        super().__init__()
        logging.getLogger(__name__)
        self.toolURL = toolURL

        self.setMaximumSize(256, 256)

        self.setObjectName('externaltool')

        style = self.style()

        self.vlayout = qtw.QVBoxLayout()

        self.optionsFrame = qtw.QFrame(parent=self)
        self.optionsFrame.setObjectName('optionsframe')
        optionsFrameLayout = qtw.QHBoxLayout()
        optionsFrameLayout.setAlignment(qt.AlignmentFlag.AlignRight)

        editIcon = style.standardIcon(style.StandardPixmap.SP_DirLinkIcon)

        self.editToolButton = qtw.QPushButton(icon=editIcon, parent=self.optionsFrame)
        self.editToolButton.setSizePolicy(qtw.QSizePolicy.Policy.Fixed, qtw.QSizePolicy.Policy.Fixed)
        self.editToolButton.setToolTip('Set slot to a different external tool')
        self.editToolButton.pressed.connect(self.editToolURL)

        deleteIcon = style.standardIcon(style.StandardPixmap.SP_DialogDiscardButton)

        self.deleteToolButton = qtw.QPushButton(icon=deleteIcon, parent=self.optionsFrame)
        self.deleteToolButton.setSizePolicy(qtw.QSizePolicy.Policy.Fixed, qtw.QSizePolicy.Policy.Fixed)
        self.deleteToolButton.setToolTip('Delete external tool shortcut')
        self.deleteToolButton.pressed.connect(self.deleteExternalTool)

        for widget in (self.editToolButton, self.deleteToolButton):
            optionsFrameLayout.addWidget(widget)

        self.optionsFrame.setLayout(optionsFrameLayout)

        self.startToolButton = qtw.QPushButton(text=self.__trimBasename(self.toolURL), parent=self)
        self.startToolButton.setSizePolicy(qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Expanding)
        self.startToolButton.setToolTip('Start external tool')
        self.startToolButton.pressed.connect(self.startExternalTool)

        for widget in (self.optionsFrame, self.startToolButton):
            self.vlayout.addWidget(widget)

        self.setLayout(self.vlayout)

    def __trimBasename(self, path: str) -> str:
        '''`os.path.basename()` includes `.exe`, this removes that'''
        return os.path.basename(path).split('.')[0]

    def editToolURL(self) -> None:
        dialog = qtw.QFileDialog()
        new_url = dialog.getOpenFileName(None, 
                                       caption='Select new external tool',
                                       filter='',
                                       selectedFilter='Executables (*.exe *.bat *.sh);;Any (*)')[0]

        if new_url:
            old_url = self.toolURL
            self.toolURL = new_url

            self.startToolButton.setText(self.__trimBasename(self.toolURL))

            self.nameChanged.emit(new_url, old_url)

    def deleteExternalTool(self, ask: bool = True) -> None:
        if ask:
            notice = DeleteModConfirmation()
            notice.warningLabel.setText('Are you sure you want to delete this shortcut?')
            notice.exec()

            if not notice.result():
                return

        self.deleted.emit(self.toolURL)

    def startExternalTool(self) -> None:
        try:
            errorChecking.startFile(self.toolURL)
        except Exception as e:
            errorMessage = 'An error has occured starting an external tool'
            logging.error('%s: %s\n%s', errorMessage, self.toolURL, str(e))

            notice = Notice(errorMessage, 'startExternalTool() Error')
            notice.exec()
