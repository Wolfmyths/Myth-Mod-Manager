import os

import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt as qt, QCoreApplication as qapp

from src.widgets.QDialog.QDialog import Dialog

from src.constant_vars import ModType

class newModLocation(Dialog):

    typeDict: dict[str : ModType] = {}
    
    def __init__(self, *modName: str) -> None:
        super().__init__()

        self.setWindowTitle(qapp.translate('newModLocation', 'Installing mods'))

        self.setMaximumSize(400, 850)
        self.setMinimumSize(320, 180)
        self.setSizePolicy(qtw.QSizePolicy.Policy.MinimumExpanding, qtw.QSizePolicy.Policy.Preferred)

        self.modName = modName
                            
        layout = qtw.QVBoxLayout()

        self.label = qtw.QLabel(
            self,
            text=qapp.translate('newModLocation', 'Please select where the mods should be installed:')
        )

        scrollArea = qtw.QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setVerticalScrollBarPolicy(qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scrollArea.setHorizontalScrollBarPolicy(qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        frame = qtw.QFrame(scrollArea)

        scrollArea.setWidget(frame)

        frameLayout = qtw.QVBoxLayout()
        frameLayout.setSpacing(5)

        for mod in (os.path.basename(x) for x in modName):

            group = qtw.QGroupBox(f'{mod}')
            group.setObjectName(mod)

            radioButtonMod = qtw.QRadioButton(ModType.mods.value, group)
            radioButtonMod.setObjectName(f'{mod} {ModType.mods}')
            radioButtonMod.setChecked(False)
            radioButtonMod.clicked.connect(self.isAllChecked)

            radioButtonOverride = qtw.QRadioButton(ModType.mods_override.value, group)
            radioButtonOverride.setObjectName(f'{mod} {ModType.mods_override}')
            radioButtonOverride.clicked.connect(self.isAllChecked)
            radioButtonOverride.setChecked(False)

            radioButtonMaps = qtw.QRadioButton(ModType.maps.value, group)
            radioButtonMaps.setObjectName(f'{mod} {ModType.maps}')
            radioButtonMaps.clicked.connect(self.isAllChecked)
            radioButtonMaps.setChecked(False)

            h1 = qtw.QHBoxLayout()
            h1.addWidget(radioButtonMod)
            h1.addWidget(radioButtonOverride)
            h1.addWidget(radioButtonMaps)

            group.setLayout(h1)

            frameLayout.addWidget(group)

        frame.setLayout(frameLayout)

        buttons = qtw.QDialogButtonBox.StandardButton.Ok | qtw.QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = qtw.QDialogButtonBox(buttons)
        self.changeOkButtonState(False)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        for widget in (self.label, scrollArea, self.buttonBox):
            layout.addWidget(widget)

        self.setLayout(layout)
    
    def changeOkButtonState(self, bool: bool) -> None:
        self.buttonBox.button(qtw.QDialogButtonBox.StandardButton.Ok).setEnabled(bool)
    
    def isAllChecked(self) -> None:

        groups: list[qtw.QGroupBox] = self.findChildren(qtw.QGroupBox)

        for group in groups:

            buttons: list[qtw.QRadioButton] = group.findChildren(qtw.QRadioButton)

            if any((buttons[0].isChecked(), buttons[1].isChecked(), buttons[2].isChecked())):
                continue
            else:
                return
        
        self.changeOkButtonState(True)

    def getData(self) -> None:

        items: list[qtw.QGroupBox] = self.findChildren(qtw.QGroupBox)

        count = 0

        # Buttons[0] is mods, buttons[1] is override, buttons[2] is Maps
        for item in items:

            buttons: list[qtw.QRadioButton] = item.findChildren(qtw.QRadioButton)

            modName = os.path.basename(self.modName[count])

            if buttons[0].isChecked():

                self.typeDict[modName] = ModType.mods
            elif buttons[1].isChecked():

                self.typeDict[modName] = ModType.mods_override
            
            elif buttons[2].isChecked():

                self.typeDict[modName] = ModType.maps

            count += 1

    def accept(self) -> None:
        self.getData()
        return super().accept()
    
    def reject(self) -> None:
        self.setResult(0)
        return super().reject()