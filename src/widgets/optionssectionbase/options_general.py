from __future__ import annotations
from typing import TYPE_CHECKING
import os

import PySide6.QtWidgets as qtw
from PySide6.QtCore import QCoreApplication as qapp, Qt, Slot

import src.helpers.helper as helper
from src.api.check_update import CheckUpdate
from src.widgets.qdialog.update_detected import UpdateDetected
from src.constant_vars import LIGHT, DARK, OptionKeys, LANG_STR_TO_CODE, ROOT_PATH
from src.helpers.options_manager import OptionsManager
from src.widgets.optionssectionbase.option_section_base import OptionsSectionBase

if TYPE_CHECKING:
    from src.widgets.qwidget.options import Options

class OptionsGeneral(OptionsSectionBase):
    def __init__(self, parent: Options = None) -> None:
        super().__init__(parent=parent)

        layout = qtw.QVBoxLayout()

        # General Sub Section
        self.general = qtw.QGroupBox(self)

        self.generalLayout = qtw.QFormLayout()
        self.generalLayout.setContentsMargins(10, 30, 10, 10)
        self.generalLayout.setVerticalSpacing(10)
        self.generalLayout.setRowWrapPolicy(qtw.QFormLayout.RowWrapPolicy.WrapAllRows)

        self.gameDir = qtw.QLineEdit(self)
        self.gameDir.textChanged.connect(self.gamePathChanged)

        self.disabledModDir = qtw.QLineEdit(self)
        self.disabledModDir.textChanged.connect(self.disPathChanged)

        self.language = qtw.QComboBox(self)
        self.language.setEditable(False)
        self.language.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.language.addItems(list(LANG_STR_TO_CODE.keys()))
        self.language.currentTextChanged.connect(self.langChanged)

        gbLayout = qtw.QHBoxLayout()

        self.buttonFrame = qtw.QGroupBox(self)
    
        self.colorThemeLight = qtw.QPushButton(self.buttonFrame)
        self.colorThemeLight.setCheckable(True)
        self.colorThemeLight.clicked.connect(lambda: self.themeChanged(LIGHT))

        self.colorThemeDark = qtw.QPushButton(self.buttonFrame)
        self.colorThemeDark.setCheckable(True)
        self.colorThemeDark.clicked.connect(lambda: self.themeChanged(DARK))

        # Button group to set exclusive check state to color theme buttons
        self.colorThemeBG = qtw.QButtonGroup(self)
        self.colorThemeBG.setExclusive(True)

        self.colorThemeBG.addButton(self.colorThemeLight, 0)
        self.colorThemeBG.addButton(self.colorThemeDark, 1)

        gbLayout.addWidget(self.colorThemeLight)
        gbLayout.addWidget(self.colorThemeDark)
        
        self.buttonFrame.setLayout(gbLayout)

        # GroupBox Updates
        self.gbUpdates = qtw.QGroupBox(self)
        gbUpdatesLayout = qtw.QVBoxLayout()

        self.updateAlertCheckbox = qtw.QCheckBox(self)
        self.updateAlertCheckbox.setChecked(OptionsManager.getMMMUpdateAlert())
        self.updateAlertCheckbox.clicked.connect(self.setUpdateAlert)

        self.CheckUpdateButton = qtw.QPushButton(self)
        self.CheckUpdateButton.clicked.connect(self.CheckUpdate)

        for widget in (self.updateAlertCheckbox, self.CheckUpdateButton):
            gbUpdatesLayout.addWidget(widget)
        
        self.gbUpdates.setLayout(gbUpdatesLayout)

        self.gameDirLabel = qtw.QLabel(self)
        self.disabledModDirLabel = qtw.QLabel(self)
        self.LanguageLabel = qtw.QLabel(self)

        # Setting rows for General Sub Section Layout
        for label, widget in (
                                (self.gameDirLabel, self.gameDir),
                                (self.disabledModDirLabel, self.disabledModDir),
                                (self.LanguageLabel, self.language)
                              ):
            self.generalLayout.addRow(label, widget)
        
        self.general.setLayout(self.generalLayout)
        
        # Setting General Section Layout
        for widget in (self.general, self.gbUpdates, self.buttonFrame):
            layout.addWidget(widget)
        
        self.applyStaticText()

        self.setLayout(layout)
    
    def applyStaticText(self) -> None:
        self.general.setTitle(qapp.translate("OptionsGeneral", "General"))

        self.buttonFrame.setTitle(qapp.translate("OptionsGeneral", "Color Theme"))
        self.colorThemeDark.setText(qapp.translate("OptionsGeneral", "Dark"))
        self.colorThemeLight.setText(qapp.translate("OptionsGeneral", "Light"))

        self.gameDirLabel.setText(qapp.translate("OptionsGeneral", "Payday 2 Game Directory:"))
        self.disabledModDirLabel.setText(qapp.translate("OptionsGeneral", "Disabled Mods Path:"))
        self.LanguageLabel.setText(qapp.translate("OptionsGeneral", "Language:"))

        self.gbUpdates.setTitle(qapp.translate("OptionsGeneral", "Updates"))
        self.updateAlertCheckbox.setText(qapp.translate("OptionsGeneral", 'Update alerts on startup'))
        self.CheckUpdateButton.setText(qapp.translate("OptionsGeneral", "Check for updates"))

    @Slot(str)
    def gamePathChanged(self, path: str) -> None:
        changed: bool = True if path != OptionsManager.getGamepath() else False
        self.pendingChanges.emit(OptionKeys.game_path, changed)
    
    @Slot(str)
    def disPathChanged(self, path: str) -> None:
        path = repr(path)
        changed: bool = True if path != OptionsManager.getDispath() else False
        self.pendingChanges.emit(OptionKeys.dispath, changed)
    
    @Slot(str)
    def langChanged(self, lang: str) -> None:
        lang = LANG_STR_TO_CODE.get(lang)
        changed: bool = True if lang != OptionsManager.getLang() else False
        self.pendingChanges.emit(OptionKeys.lang, changed)
    
    @Slot(str)
    def themeChanged(self, theme: str) -> None:
        changed: bool = True if theme != OptionsManager.getTheme() else False
        self.pendingChanges.emit(OptionKeys.color_theme, changed)
    
    @Slot()
    def setUpdateAlert(self) -> None:
        changed: bool = True if self.updateAlertCheckbox.isChecked() != OptionsManager.getMMMUpdateAlert() else False
        self.pendingChanges.emit(OptionKeys.mmm_update_alert, changed)
    
    def CheckUpdate(self) -> None:
        @Slot(str, str)
        def updateFound(latestVersion: str, changelog: str) -> None:
            notice = UpdateDetected(latestVersion, changelog)
            notice.rejected.connect(lambda: self.CheckUpdateButton.setText(qapp.translate("OptionsGeneral", 'Check for updates')))
            notice.exec()
            
            if notice.result():
                helper.startFile(os.path.join(ROOT_PATH, 'Myth Mod Manager.exe'))
                qapp.quit()

        self.CheckUpdateButton.setText(qapp.translate("OptionsGeneral", 'Checking...'))

        self.run_CheckUpdate = CheckUpdate()
        self.run_CheckUpdate.updateDetected.connect(updateFound)
        self.run_CheckUpdate.error.connect(lambda: self.CheckUpdateButton.setText(qapp.translate("OptionsGeneral", 'Error: Check logs for more info')))
        self.run_CheckUpdate.upToDate.connect(lambda: self.CheckUpdateButton.setText(qapp.translate("OptionsGeneral", 'Up to date!' ) + ' ^_^' ))