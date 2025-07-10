from __future__ import annotations
from typing import TYPE_CHECKING

import PySide6.QtWidgets as qtw
from PySide6.QtCore import QCoreApplication as qapp, Slot

import src.helpers.helper as helper
from src.constant_vars import OptionKeys
from src.widgets.optionssectionbase.option_section_base import OptionsSectionBase

if TYPE_CHECKING:
    from src.widgets.qwidget.options import Options

class OptionsLaunchParams(OptionsSectionBase):
    def __init__(self, parent: Options = None) -> None:
        super().__init__(parent)
        layout = qtw.QVBoxLayout()
        childLayout = qtw.QFormLayout()
        childLayout.setContentsMargins(0, 0, 300, 20)
        childLayout.setVerticalSpacing(10)
        childLayout2 = qtw.QFormLayout()
        childLayout2.setVerticalSpacing(10)
        childLayout2.setSpacing(10)
        childLayout2.setRowWrapPolicy(qtw.QFormLayout.RowWrapPolicy.WrapAllRows)

        self.warningLabel         = qtw.QLabel(qapp.translate("OptionsLaunchParams", "USE THESE IF YOU KNOW WHAT YOU'RE DOING"), self)
        
        self.dLineEdit            = qtw.QLineEdit(self)
        self.dLineEdit.setPlaceholderText("<dir>")
        self.oLineEdit            = qtw.QLineEdit(self)
        self.oLineEdit.setPlaceholderText("<file>")
        
        self.sCheckBox            = qtw.QCheckBox(self)
        self.uCheckBox            = qtw.QCheckBox(self)
        self.qCheckBox            = qtw.QCheckBox(self)
        self.skipintroCheckBox    = qtw.QCheckBox(self)
        self.steamMMCheckBox      = qtw.QCheckBox(self)
        self.epicMMCheckBox       = qtw.QCheckBox(self)
        self.newCPUCheckBox       = qtw.QCheckBox(self)
        self.qaCheckBox           = qtw.QCheckBox(self)
        self.crashCheckBox        = qtw.QCheckBox(self)
        self.delayedstartCheckBox = qtw.QCheckBox(self)
        self.removevtuneCheckBox  = qtw.QCheckBox(self)

        self.customLineEdit       = qtw.QLineEdit(self)
        self.previewLineEdit      = qtw.QLineEdit(self)
        self.previewLineEdit.setReadOnly(True)

        
        launchParamPairs: tuple[tuple[str, qtw.QWidget], ...] = self._get_param_widget_pairs()

        # Assigning for child layout 1
        for title, widget in launchParamPairs:
            childLayout.addRow(title, widget)
            widget.setProperty("param", title)

            if isinstance(widget, qtw.QCheckBox):
                widget.clicked.connect(self.update_preview)
            elif isinstance(widget, qtw.QLineEdit):
                widget.textEdited.connect(self.update_preview)
        
        self.setup()
        
        self.customLineEdit.textEdited.connect(self.update_preview)

        # Assigning for child layout 2
        for title, widget in (
            (qapp.translate("OptionsLaunchParams", "Custom Args:"), self.customLineEdit),
            (qapp.translate("OptionsLaunchParams", "Preview:"), self.previewLineEdit)
        ):
            childLayout2.addRow(title, widget)

        self.previewLineEdit.textChanged.connect(self.on_preview_text_changed)

        layout.addWidget(self.warningLabel)
        layout.addLayout(childLayout)
        layout.addLayout(childLayout2)
        self.setLayout(layout)
    
    def setup(self) -> None:
        launchParamPairs: tuple[tuple[str, qtw.QWidget], ...] = self._get_param_widget_pairs()
        launch_parameters: list[str] = helper.launchParamsToList()

        for title, lineEdit in launchParamPairs[:2]:
            lineEdit: qtw.QLineEdit
            for param in launch_parameters:
                if param.startswith(title):
                    lineEdit.setText(param)
                    launch_parameters.remove(param)
                else:
                    lineEdit.setText('')
        
        for title, checkBox in launchParamPairs[3:]:
            checkBox: qtw.QCheckBox
            if title in launch_parameters:
                checkBox.setChecked(True)
                launch_parameters.remove(title)
            else:
                checkBox.setChecked(False)
        
        self.customLineEdit.setText(' '.join(launch_parameters))
        self.update_preview()


    def _get_param_widget_pairs(self) -> tuple[tuple[str, qtw.QWidget], ...]:
        return (
            ('-d', self.dLineEdit),
            ('-o', self.oLineEdit),
            ('-u', self.uCheckBox),
            ('-q', self.qCheckBox),
            ('-s', self.sCheckBox),
            ('-skip_intro', self.skipintroCheckBox),
            ('-steamMM', self.steamMMCheckBox),
            ('-epicMM', self.epicMMCheckBox),
            ('-NewCPU', self.newCPUCheckBox),
            ('-qa', self.qaCheckBox),
            ('-crash', self.crashCheckBox),
            ('-delayedstart', self.delayedstartCheckBox),
            ('-removevtune', self.removevtuneCheckBox)
        )

    @Slot(str)
    def on_preview_text_changed(self, newText: str) -> None:
        newText: str = newText.strip()

        newTextSet: set[str]
        if newText:
            newTextSet = set(helper.launchParamsToList(newText))
        else:
            newTextSet = set()
        
        currentTextSet: set[str] = set(helper.launchParamsToList())

        is_changed: bool = not newTextSet == currentTextSet
        
        #print(
        #    "New Text: ", newTextSet, '\n',
        #    "Current Text: ", currentTextSet, '\n',
        #    "Is same: ", newTextSet == currentTextSet
        #)
        
        self.pendingChanges.emit(OptionKeys.launch_parameters.value, is_changed)

    @Slot()
    def update_preview(self) -> None:
        args: list[str] = []

        if self.customLineEdit.text():
            args.append(self.customLineEdit.text())

        for lineedit in (self.dLineEdit, self.oLineEdit):
            lineedit: qtw.QLineEdit
            if lineedit.text():
                args.append(f'{lineedit.property("param")} {lineedit.text()}')

        for checkbox in self.findChildren(qtw.QCheckBox):
            checkbox: qtw.QCheckBox
            if checkbox.isChecked():
                args.append(checkbox.property("param"))
        
        self.previewLineEdit.setText(' '.join(args))