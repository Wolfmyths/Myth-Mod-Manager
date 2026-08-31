from typing import LiteralString, cast

import PySide6.QtWidgets as qtw
from PySide6.QtCore import QCoreApplication as qapp, Slot

from src.constant_vars import OptionKeys
from src.helpers.options_manager import OptionsManager
from src.widgets.optionssectionbase.option_section_base import OptionsSectionBase

class OptionsLaunchParams(OptionsSectionBase):
    def __init__(self, parent: qtw.QWidget | None = None) -> None:
        super().__init__(parent)
        layout = qtw.QVBoxLayout()
        childLayout = qtw.QFormLayout()
        childLayout.setContentsMargins(0, 0, 300, 20)
        childLayout.setVerticalSpacing(10)
        childLayout2 = qtw.QFormLayout()
        childLayout2.setVerticalSpacing(10)
        childLayout2.setSpacing(10)
        childLayout2.setRowWrapPolicy(qtw.QFormLayout.RowWrapPolicy.WrapAllRows)

        PARAM: LiteralString = "param"

        self.warningLabel            = qtw.QLabel(qapp.translate("OptionsLaunchParams", "USE THESE IF YOU KNOW WHAT YOU'RE DOING"), self)
        
        self.dLineEdit            = qtw.QLineEdit(self, placeholderText="<dir>")
        self.dLineEdit.setProperty(PARAM, "-d")
        self.oLineEdit            = qtw.QLineEdit(self, placeholderText="<file>")
        self.oLineEdit.setProperty(PARAM, "-o")
        
        self.sCheckBox            = qtw.QCheckBox(self)
        self.sCheckBox.setProperty(PARAM, "-s")
        self.uCheckBox            = qtw.QCheckBox(self)
        self.uCheckBox.setProperty(PARAM, "-u")
        self.qCheckBox            = qtw.QCheckBox(self)
        self.qCheckBox.setProperty(PARAM, "-q")
        self.skipintroCheckBox    = qtw.QCheckBox(self)
        self.skipintroCheckBox.setProperty(PARAM, "-skip_intro")
        self.steamMMCheckBox      = qtw.QCheckBox(self)
        self.steamMMCheckBox.setProperty(PARAM, "-steamMM")
        self.epicMMCheckBox       = qtw.QCheckBox(self)
        self.epicMMCheckBox.setProperty(PARAM, "-epicMM")
        self.newCPUCheckBox       = qtw.QCheckBox(self)
        self.newCPUCheckBox.setProperty(PARAM, "-NewCPU")
        self.qaCheckBox           = qtw.QCheckBox(self)
        self.qaCheckBox.setProperty(PARAM, "-qa")
        self.crashCheckBox        = qtw.QCheckBox(self)
        self.crashCheckBox.setProperty(PARAM, "-crash")
        self.delayedstartCheckBox = qtw.QCheckBox(self)
        self.delayedstartCheckBox.setProperty(PARAM, "-delayedstart")
        self.removevtuneCheckBox  = qtw.QCheckBox(self)
        self.removevtuneCheckBox.setProperty(PARAM, "-removevtune")

        self.customLineEdit       = qtw.QLineEdit(self)
        self.previewLineEdit      = qtw.QLineEdit(self, readOnly=True)
        
        launchParamPairs = self._get_param_widget_pairs()

        # Assigning for child layout 1
        for title, widget in launchParamPairs:
            childLayout.addRow(title, widget)

            if isinstance(widget, qtw.QCheckBox):
                widget.clicked.connect(self.update_preview)
            else:
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
        launchParamPairs = self._get_param_widget_pairs()
        lineEditPairs = [x for x in launchParamPairs if isinstance(x[1], qtw.QLineEdit)]
        checkboxPairs = [x for x in launchParamPairs if isinstance(x[1], qtw.QCheckBox)]
        launch_parameters = OptionsManager.getLaunchParameters().split("-")

        def _find_arg(arg: str) -> int:
            for idx in range(len(launch_parameters)):
                if not launch_parameters[idx].startswith(arg):
                    continue
                
                return idx

            return -1

        for title, lineEdit in lineEditPairs:
            lineEdit = cast(qtw.QLineEdit, lineEdit)
            idx = _find_arg(title)
            if not idx == -1:
                lineEdit.setText(f"-{launch_parameters[idx]}")
            else:
                lineEdit.clear()
        
        for title, checkBox in checkboxPairs:
            checkBox = cast(qtw.QCheckBox, checkBox)
            checkBox.setChecked(not _find_arg(title) == -1)
        
        self.customLineEdit.setText(' '.join(launch_parameters))
        self.update_preview()


    def _get_param_widget_pairs(self) -> tuple[tuple[str, qtw.QCheckBox | qtw.QLineEdit], ...]:
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
        newText = newText.strip()
        currentText = OptionsManager.getLaunchParameters()

        is_changed: bool = not newText == currentText
        
        print(
            "On preview text changed triggered",
            "New Text: ", newText, '\n',
            "Current Text: ", currentText, '\n',
            "Is same: ", newText == currentText
        )
        
        self.pendingChanges.emit(OptionKeys.launch_parameters, is_changed)

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