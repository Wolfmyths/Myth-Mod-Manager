import os
import logging

import PySide6.QtGui as qtg
from PySide6.QtCore import Qt as qt, QSize
import PySide6.QtWidgets as qtw

from src.save import OptionsManager
from src.errorChecking import openWebPage

from src.constant_vars import VERSION, PROGRAM_NAME, UI_GRAPHICS_PATH, GITHUB_LOGO_W, GITHUB_LOGO_B, LIGHT, OPTIONS_THEME, MODWORKSHOP_LOGO_B, MODWORKSHOP_LOGO_W, KOFI_LOGO_B


class About(qtw.QWidget):
    def __init__(self) -> None:
        super().__init__()

        logging.getLogger(__file__)

        self.options = OptionsManager()

        layout = qtw.QVBoxLayout()
        layout.setAlignment(qt.AlignmentFlag.AlignTop)

        self.buttonFrame = qtw.QFrame(self)

        self.githubLabel = qtw.QPushButton(self.buttonFrame)
        self.kofiLabel = qtw.QPushButton(self.buttonFrame)
        self.modworkshopLabel = qtw.QPushButton(self.buttonFrame)

        self.githubLabel.setToolTip('Visit Github Repository')
        self.kofiLabel.setToolTip('Support Wolfmyths on Ko-Fi')
        self.modworkshopLabel.setToolTip('Visit Modworkshop Page')

        self.githubLabel.clicked.connect(lambda: openWebPage('https://github.com/Wolfmyths/Myth-Mod-Manager'))
        self.kofiLabel.clicked.connect(lambda: openWebPage('https://ko-fi.com/C0C4MJZS9'))
        self.modworkshopLabel.clicked.connect(lambda: openWebPage('https://modworkshop.net/mod/43276'))

        buttonFrameLayout = qtw.QHBoxLayout()
        buttonFrameLayout.setAlignment(qt.AlignmentFlag.AlignTop)

        for widget in (self.githubLabel, self.kofiLabel, self.modworkshopLabel):
            widget.setIconSize(QSize(98, 96))
            buttonFrameLayout.addWidget(widget)
        
        self.buttonFrame.setLayout(buttonFrameLayout)

        self.updateIcons()

        self.aboutLabel = qtw.QLabel(self, text=
f'''
{PROGRAM_NAME} {VERSION} is an open-source mod manager for PAYDAY 2 created by Wolfmyths

The goal of this program is to streamline the proccess of PAYDAY 2 mod managment
without hassle of juggling multiple file explorers.

Suggestions are greatly appreciated on modworkshop.net

''')
        self.aboutLabel.setWordWrap(True)
        self.aboutLabel.setAlignment(qt.AlignmentFlag.AlignTop)

        self.shortcutsLabel = qtw.QLabel(self)
        self.shortcutsLabel.setText('Shortcuts:\n\n+ Select All: Ctrl + A\n\n+ Deselect All: Ctrl + D\n\n+ Delete Mod or Profile: Del\n\n+ Change Profile Name: Enter')
        self.shortcutsLabel.setTextFormat(qt.TextFormat.MarkdownText)

        for widget in (self.buttonFrame, self.aboutLabel, self.shortcutsLabel):
            layout.addWidget(widget)

        self.setLayout(layout)
    
    def updateIcons(self) -> None:

        themeIsLight: bool = self.options.getOption(OPTIONS_THEME, LIGHT) == LIGHT

        self.githubIcon = GITHUB_LOGO_B if themeIsLight else GITHUB_LOGO_W
        self.kofiIcon = KOFI_LOGO_B
        self.modworkshopIcon = MODWORKSHOP_LOGO_B if themeIsLight else MODWORKSHOP_LOGO_W

        githubPixmap = qtg.QIcon(os.path.join(UI_GRAPHICS_PATH, self.githubIcon))

        kofiPixmap = qtg.QIcon(os.path.join(UI_GRAPHICS_PATH, self.kofiIcon))

        modworkshopPixmap = qtg.QIcon(os.path.join(UI_GRAPHICS_PATH, self.modworkshopIcon))

        self.githubLabel.setIcon(githubPixmap)
        self.kofiLabel.setIcon(kofiPixmap)
        self.modworkshopLabel.setIcon(modworkshopPixmap)
