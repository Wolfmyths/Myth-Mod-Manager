import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt as qt

from src.widgets.toolQWidget import ExternalToolDisplay

class ToolManager(qtw.QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = qtw.QVBoxLayout()

        self.addToolButton = qtw.QPushButton(text='Add Tool')
        self.addToolButton.setLayoutDirection(qt.LayoutDirection.RightToLeft)
        self.addToolButton.clicked.connect(self.createTools)

        self.toolsWidget = ExternalToolDisplay()

        for widget in (self.addToolButton, self.toolsWidget):
            layout.addWidget(widget)

        self.setLayout(layout)
    
    def createTools(self) -> None:
        dialog = qtw.QFileDialog()
        urls = dialog.getOpenFileNames(self, 
                                       caption='Select External Tool(s)', 
                                       filter='Executables (*.exe *.bat)')[0]

        if urls:
            self.toolsWidget.addTool(*urls)