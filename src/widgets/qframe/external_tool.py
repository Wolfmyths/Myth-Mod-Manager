import os
import logging

from PySide6.QtGui import QIcon
import PySide6.QtWidgets as qtw
from PySide6.QtCore import QUrl, Qt as qt, Signal, QCoreApplication as qapp, Slot

from src.widgets.qdialog.notice import Notice
from src.widgets.qdialog.confirmation import Confirmation

from src.helpers import helper

class ExternalTool(qtw.QFrame):
    deleted = Signal(str)
    nameChanged = Signal(str, str)
    def __init__(self, toolURL: str) -> None:
        super().__init__()
        logging.getLogger(__name__)
        self.toolURL: str = toolURL

        self.setMaximumSize(256, 256)

        self.setObjectName('externaltool')

        style: qtw.QStyle = self.style()

        self.vlayout = qtw.QVBoxLayout()

        self.optionsFrame = qtw.QFrame(parent=self)
        self.optionsFrame.setObjectName('optionsframe')
        optionsFrameLayout = qtw.QHBoxLayout()
        optionsFrameLayout.setAlignment(qt.AlignmentFlag.AlignRight)

        editIcon: QIcon = style.standardIcon(style.StandardPixmap.SP_DirLinkIcon)

        self.editToolButton = qtw.QPushButton(editIcon, '', parent=self.optionsFrame)
        self.editToolButton.setSizePolicy(qtw.QSizePolicy.Policy.Fixed, qtw.QSizePolicy.Policy.Fixed)
        self.editToolButton.pressed.connect(self.editToolURL)

        deleteIcon: QIcon = style.standardIcon(style.StandardPixmap.SP_DialogDiscardButton)

        self.deleteToolButton = qtw.QPushButton(deleteIcon, '', parent=self.optionsFrame)
        self.deleteToolButton.setSizePolicy(qtw.QSizePolicy.Policy.Fixed, qtw.QSizePolicy.Policy.Fixed)
        self.deleteToolButton.pressed.connect(self.deleteExternalTool)

        for widget in (self.editToolButton, self.deleteToolButton):
            optionsFrameLayout.addWidget(widget)

        self.optionsFrame.setLayout(optionsFrameLayout)

        self.startToolButton = qtw.QPushButton(self.__trimBasename(self.toolURL), parent=self)
        self.startToolButton.setSizePolicy(qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Expanding)
        self.startToolButton.pressed.connect(self.startExternalTool)

        for widget in (self.optionsFrame, self.startToolButton):
            self.vlayout.addWidget(widget)

        self.setLayout(self.vlayout)

        self.applyStaticText()
    
    def applyStaticText(self) -> None:
        self.editToolButton.setToolTip(qapp.translate('ExternalTool', 'Set slot to a different external tool'))
        self.deleteToolButton.setToolTip(qapp.translate('ExternalTool', 'Delete external tool shortcut'))
        self.startToolButton.setToolTip(qapp.translate('ExternalTool', 'Start external tool'))

    def __trimBasename(self, path: str) -> str:
        '''`os.path.basename()` includes `.exe`, this removes that'''
        return os.path.basename(path).split('.')[0]

    @Slot()
    def editToolURL(self) -> None:
        dialog = qtw.QFileDialog()
        new_url: tuple[QUrl, str] = dialog.getOpenFileUrl(
            None, 
            caption=qapp.translate('ExternalTool', 'Select new external tool'),
            filter=qapp.translate('ExternalTool', 'Executables') + '(*.exe *.bat *.sh);;Any (*)'
        )
        
        new_urlLocalFile: str = new_url[0].toLocalFile()

        if os.path.isfile(new_urlLocalFile):
            old_url: str = self.toolURL
            self.toolURL = new_urlLocalFile

            self.startToolButton.setText(self.__trimBasename(self.toolURL))

            self.nameChanged.emit(new_urlLocalFile, old_url)

    @Slot()
    @Slot(bool)
    def deleteExternalTool(self, ask: bool = True) -> None:
        if ask:
            notice = Confirmation(
                qapp.translate('ExternalTool','Delete tool shortcut'),
                qapp.translate('ExternalTool','Are you sure you want to delete this shortcut?')
            )
            notice.exec()

            if notice.result():
                self.deleted.emit(self.toolURL)

    @Slot()
    def startExternalTool(self) -> None:
        try:
            helper.startFile(self.toolURL)
        except Exception as e:
            logging.error('%s: %s\n%s', 'An error was raised starting an external tool', self.toolURL, str(e))

            notice = Notice(
                qapp.translate('ExternalTool', 'An error was raised starting an external tool'),
                'startExternalTool() ' + qapp.translate('ExternalTool', 'Error')
            )
            notice.exec()
