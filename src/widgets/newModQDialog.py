
from constant_vars import TYPE_MODS, TYPE_MODS_OVERRIDE

import PySide6.QtWidgets as qtw

class newModLocation(qtw.QDialog):
    def __init__(self, modName: str) -> None:
        super().__init__()

        self.setWindowTitle('Installing mod')

        layout = qtw.QVBoxLayout()

        warningLabel = qtw.QLabel(self, text=f'What type of mod is {modName}?')

        buttonFrame = qtw.QFrame(self)
        frameLayout = qtw.QHBoxLayout()

        modsButton = qtw.QPushButton(parent=buttonFrame, text=TYPE_MODS)
        modsButton.clicked.connect(lambda: self.accept(TYPE_MODS))

        overrideButton = qtw.QPushButton(parent=buttonFrame, text=TYPE_MODS_OVERRIDE)
        overrideButton.clicked.connect(lambda: self.accept(TYPE_MODS_OVERRIDE))

        cancelButton = qtw.QPushButton(parent=buttonFrame, text='Cancel')
        cancelButton.clicked.connect(lambda: self.reject())

        for widget in (modsButton, overrideButton, cancelButton):

            frameLayout.addWidget(widget)
        
        buttonFrame.setLayout(frameLayout)

        for widget in (warningLabel, buttonFrame):
            layout.addWidget(widget)
        
        self.setLayout(layout)
    
    def accept(self, type: str) -> None:

        self.type = type

        return super().accept()
    
    def reject(self) -> None:
        self.type = 0
        return super().reject()