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
        nameFilters = ['Executables (*.exe, *.bat)', 'Any (*)']
        dialog = qtw.QFileDialog()
        dialog.setFileMode(dialog.FileMode.ExistingFile)
        dialog.setNameFilters(nameFilters)
        dialog.selectNameFilter(nameFilters[0])
        dialog.setWindowTitle('Select External Tool')
        dialog.setLabelText(dialog.DialogLabel.Accept, 'Select')

        dialog.exec()

        new_url = dialog.selectedUrls()

        if dialog.result() and new_url:
            self.toolsWidget.addTool(*[x.toLocalFile() for x in new_url])