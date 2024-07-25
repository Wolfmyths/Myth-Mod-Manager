import os
import logging

import PySide6.QtGui as qtg
from PySide6.QtCore import Qt as qt, QSize, QCoreApplication as qapp, Slot
import PySide6.QtWidgets as qtw

from src.save import OptionsManager
from src.errorChecking import openWebPage

from src.constant_vars import VERSION, PROGRAM_NAME, UI_GRAPHICS_PATH, GITHUB_LOGO_W, GITHUB_LOGO_B, LIGHT, MODWORKSHOP_LOGO_B, MODWORKSHOP_LOGO_W, KOFI_LOGO_B, OPTIONS_CONFIG


class About(qtw.QWidget):
    def __init__(self, optionsPath: str = OPTIONS_CONFIG) -> None:
        super().__init__()

        logging.getLogger(__file__)

        self.options = OptionsManager(optionsPath)

        layout = qtw.QVBoxLayout()
        layout.setAlignment(qt.AlignmentFlag.AlignTop)

        self.buttonFrame = qtw.QFrame(self)

        self.githubLabel = qtw.QPushButton(self.buttonFrame)
        self.kofiLabel = qtw.QPushButton(self.buttonFrame)
        self.modworkshopLabel = qtw.QPushButton(self.buttonFrame)

        self.githubLabel.clicked.connect(lambda: openWebPage('https://github.com/Wolfmyths/Myth-Mod-Manager'))
        self.kofiLabel.clicked.connect(lambda: openWebPage('https://ko-fi.com/C0C4MJZS9'))
        self.modworkshopLabel.clicked.connect(lambda: openWebPage('https://modworkshop.net/mod/43276'))

        buttonFrameLayout = qtw.QHBoxLayout()
        buttonFrameLayout.setAlignment(qt.AlignmentFlag.AlignTop)

        for widget in (self.githubLabel, self.kofiLabel, self.modworkshopLabel):
            widget.setIconSize(QSize(98, 96))
            buttonFrameLayout.addWidget(widget)
        
        self.buttonFrame.setLayout(buttonFrameLayout)

        self.updateIcons(self.options.getTheme())

        self.aboutLabel = qtw.QLabel(self)
        self.aboutLabel.setWordWrap(True)
        self.aboutLabel.setContentsMargins(30,0,30,0)
        self.aboutLabel.setAlignment(qt.AlignmentFlag.AlignTop)

        for widget in (self.buttonFrame, self.aboutLabel):
            layout.addWidget(widget)

        self.applyStaticText()

        self.setLayout(layout)
    
    def applyStaticText(self) -> None:
        self.githubLabel.setToolTip(qapp.translate('About', 'Visit Github Repository'))
        self.kofiLabel.setToolTip(qapp.translate('About', 'Support Wolfmyths on Ko-Fi'))
        self.modworkshopLabel.setToolTip(qapp.translate('About','Visit Modworkshop Page'))

        self.aboutLabel.setText('\n\n'.join([
            '',
            f'{PROGRAM_NAME} {VERSION} ' + qapp.translate('About', 'is an open-source mod manager for PAYDAY 2 created by Wolfmyths.'),
            qapp.translate('About', 'The goal of this program is to streamline the proccess of PAYDAY 2 mod managment without hassle of juggling multiple file explorers.'),
            qapp.translate('About', 'Suggestions are greatly appreciated on modworkshop.net and github.')
        ]))
    
    @Slot(str)
    def updateIcons(self, mode: str) -> None:

        themeIsLight: bool = mode == LIGHT

        self.githubIcon = GITHUB_LOGO_B if themeIsLight else GITHUB_LOGO_W
        self.kofiIcon = KOFI_LOGO_B
        self.modworkshopIcon = MODWORKSHOP_LOGO_B if themeIsLight else MODWORKSHOP_LOGO_W

        githubPixmap = qtg.QIcon(os.path.join(UI_GRAPHICS_PATH, self.githubIcon))

        kofiPixmap = qtg.QIcon(os.path.join(UI_GRAPHICS_PATH, self.kofiIcon))

        modworkshopPixmap = qtg.QIcon(os.path.join(UI_GRAPHICS_PATH, self.modworkshopIcon))

        self.githubLabel.setIcon(githubPixmap)
        self.kofiLabel.setIcon(kofiPixmap)
        self.modworkshopLabel.setIcon(modworkshopPixmap)
