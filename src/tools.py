import os

import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt as qt, QCoreApplication as qapp

from src.widgets.toolQWidget import ExternalToolDisplay

class ToolManager(qtw.QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = qtw.QVBoxLayout()

        self.addToolButton = qtw.QPushButton(self)
        self.addToolButton.setLayoutDirection(qt.LayoutDirection.RightToLeft)
        self.addToolButton.clicked.connect(self.createTools)

        self.toolsWidget = ExternalToolDisplay()

        for widget in (self.addToolButton, self.toolsWidget):
            layout.addWidget(widget)

        self.setLayout(layout)

        self.applyStaticText()
    
    def applyStaticText(self) -> None:
        self.addToolButton.setText(qapp.translate("ToolManager", "Add Tool"))

    def createTools(self) -> None:
        dialog = qtw.QFileDialog()
        urls = dialog.getOpenFileUrl(self,
                                       caption=qapp.translate("ToolManager", 'Select External Tool(s)'), 
                                       filter=qapp.translate("ToolManager", 'Executables') + '(*.exe *.bat *.sh);;Any (*)')
        
        new_url = urls[0].toLocalFile()

        if os.path.isfile(new_url):
            self.toolsWidget.addTool(new_url)