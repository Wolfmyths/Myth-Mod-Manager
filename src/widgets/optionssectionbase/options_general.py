import os
import logging
import platform

import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
from PySide6.QtCore import QCoreApplication as qapp, QFileInfo, QModelIndex, QStringListModel, Qt, Slot
from typing_extensions import override

import src.helpers.helper as helper
from src.api.check_update import CheckUpdate
from src.widgets.qdialog.update_detected import UpdateDetected
from src.constant_vars import LIGHT, DARK, OptionKeys, LANG_STR_TO_CODE, ROOT_PATH, STEAM
from src.helpers.options_manager import OptionsManager
from src.widgets.optionssectionbase.option_section_base import OptionsSectionBase

class OptionsGeneral(OptionsSectionBase):
    def __init__(self, parent: qtw.QWidget | None = None) -> None:
        super().__init__(parent=parent)

        layout = qtw.QVBoxLayout()

        self.run_CheckUpdate = CheckUpdate(self)
        self.run_CheckUpdate.updateDetected.connect(self.updateFound)
        self.run_CheckUpdate.error.connect(lambda: self.CheckUpdateButton.setText(qapp.translate("OptionsGeneral", 'Error: Check logs for more info')))
        self.run_CheckUpdate.upToDate.connect(lambda: self.CheckUpdateButton.setText(qapp.translate("OptionsGeneral", 'Up to date!' ) + ' ^_^' ))

        # General Sub Section
        self.general = qtw.QGroupBox(self)

        self.generalLayout = qtw.QFormLayout(
            rowWrapPolicy=qtw.QFormLayout.RowWrapPolicy.WrapAllRows,
            verticalSpacing=10,
        )
        self.generalLayout.setContentsMargins(10, 30, 10, 10)

        self.gameDir = qtw.QLineEdit(self)
        self.gameDir.textChanged.connect(self.gamePathChanged)

        self.disabledModDir = qtw.QLineEdit(self)
        self.disabledModDir.textChanged.connect(self.disPathChanged)

        available_proton_versions: list[str] = ["N/A"]
        if platform.system() == "Linux":
            if os.path.isdir(STEAM):
                available_proton_versions = helper.findProtonVersions()

                # Select the latest installed version if the option isn't set
                if not OptionsManager.getProtonVersion():
                    OptionsManager.setProtonVersion(available_proton_versions[0])
            else:
                logging.error("Could not find steam directory! %s", STEAM)

        self.language = qtw.QComboBox(self, editable=False)
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

        # Proton Settings Subgroup (Linux Only)
        protonLayout = qtw.QVBoxLayout()
        protonDirButtonLayout = qtw.QHBoxLayout()
        protonDirButtonLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.protonGroupBox = qtw.QGroupBox(self)

        self.protonVerComboBox = qtw.QComboBox(self.protonGroupBox, editable=False)
        self.protonVerComboBox.addItems(available_proton_versions)
        self.protonVerComboBox.currentTextChanged.connect(self.protonVerChanged)

        addIcon = qtg.QIcon.fromTheme(qtg.QIcon.ThemeIcon.ListAdd)
        removeIcon = qtg.QIcon.fromTheme(qtg.QIcon.ThemeIcon.ListRemove)

        self.protonDirsButtonAdd = qtw.QPushButton(addIcon, "", self.protonGroupBox)
        self.protonDirsButtonAdd.pressed.connect(self.addProtonDir)
        protonDirButtonLayout.addWidget(self.protonDirsButtonAdd)

        self.protonDirsButtonRemove = qtw.QPushButton(removeIcon, "", self.protonGroupBox)
        self.protonDirsButtonRemove.pressed.connect(self.removeProtonDir)
        protonDirButtonLayout.addWidget(self.protonDirsButtonRemove)

        self.protonDirsModel = QStringListModel(OptionsManager.getProtonDirs(), self)
        self.protonDirsModel.dataChanged.connect(self.protonDirsDataChanged)
        self.protonDirsListView = qtw.QListView(
            self.protonGroupBox, 
            viewMode=qtw.QListView.ViewMode.ListMode,
            flow=qtw.QListView.Flow.TopToBottom)
        self.protonDirsListView.setEditTriggers(qtw.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.protonDirsListView.setModel(self.protonDirsModel)

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
        self.protonLabel = qtw.QLabel(self)
        self.protonDirsLabel = qtw.QLabel(self)
        self.LanguageLabel = qtw.QLabel(self)

        # Setting rows for General Sub Section Layout
        for label, widget in (
                                (self.gameDirLabel, self.gameDir),
                                (self.disabledModDirLabel, self.disabledModDir),
                                (self.LanguageLabel, self.language)
                              ):
            self.generalLayout.addRow(label, widget)
        
        self.general.setLayout(self.generalLayout)
        
        # Setting rows for Proton Sub Section Layout
        protonLayout.addWidget(self.protonLabel)
        protonLayout.addWidget(self.protonVerComboBox)
        protonLayout.addWidget(self.protonDirsLabel)
        protonLayout.addLayout(protonDirButtonLayout)
        protonLayout.addWidget(self.protonDirsListView)
        self.protonGroupBox.setLayout(protonLayout)

        # Setting General Section Layout
        for widget in (self.general, self.protonGroupBox, self.gbUpdates, self.buttonFrame):
            layout.addWidget(widget)
        
        self.applyStaticText()

        self.setLayout(layout)
    
    @override
    def applyStaticText(self) -> None:
        self.general.setTitle(qapp.translate("OptionsGeneral", "General"))

        self.buttonFrame.setTitle(qapp.translate("OptionsGeneral", "Color Theme"))
        self.colorThemeDark.setText(qapp.translate("OptionsGeneral", "Dark"))
        self.colorThemeLight.setText(qapp.translate("OptionsGeneral", "Light"))

        self.gameDirLabel.setText(qapp.translate("OptionsGeneral", "Payday 2 Game Path:"))
        self.disabledModDirLabel.setText(qapp.translate("OptionsGeneral", "Disabled Mods Path:"))
        self.LanguageLabel.setText(qapp.translate("OptionsGeneral", "Language:"))

        self.protonGroupBox.setTitle(qapp.translate("OptionsGeneral", "Proton"))
        self.protonLabel.setText(qapp.translate("OptionsGeneral", "Version:"))
        self.protonDirsLabel.setText(qapp.translate("OptionsGeneral", "Custom Proton Directories:"))

        self.gbUpdates.setTitle(qapp.translate("OptionsGeneral", "Updates"))
        self.updateAlertCheckbox.setText(qapp.translate("OptionsGeneral", 'Update alerts on startup'))
        self.CheckUpdateButton.setText(qapp.translate("OptionsGeneral", "Check for updates"))

    @Slot(str, str)
    def updateFound(self, latestVersion: str, changelog: str) -> None:
        notice = UpdateDetected(latestVersion, changelog)
        notice.rejected.connect(lambda: self.CheckUpdateButton.setText(qapp.translate("OptionsGeneral", 'Check for updates')))
        notice.exec()
        
        if notice.result():
            helper.startFile(os.path.join(ROOT_PATH, 'Myth Mod Manager.exe'))
            qapp.quit()

    @Slot()
    def addProtonDir(self) -> None:
        url = qtw.QFileDialog.getExistingDirectoryUrl(
            self,
            caption=qapp.translate('OptionsGeneral', 'Select a Location Where Proton Versions Are Stored')
        ).toLocalFile()

        if not QFileInfo(url).exists():
            return
        
        self.protonDirsModel.setStringList(self.protonDirsModel.stringList() + [url])

    @Slot()
    def removeProtonDir(self) -> None:
        for qmodelindex in self.protonDirsListView.selectedIndexes():
            self.protonDirsModel.removeRow(qmodelindex.row())

    @Slot(QModelIndex, QModelIndex, list)
    def protonDirsDataChanged(self, _topLeft: QModelIndex, _bottomRight: QModelIndex, _roles: list[int]) -> None:
        changed: bool = self.protonDirsModel.stringList() != OptionsManager.getProtonDirs()
        self.pendingChanges.emit(OptionKeys.proton_dirs, changed)

    @Slot(str)
    def protonVerChanged(self, version: str) -> None:
        changed: bool = version != OptionsManager.getProtonVersion()
        self.pendingChanges.emit(OptionKeys.proton_version, changed)

    @Slot(str)
    def gamePathChanged(self, path: str) -> None:
        changed: bool = path != OptionsManager.getGamepath()
        self.pendingChanges.emit(OptionKeys.game_path, changed)
    
    @Slot(str)
    def disPathChanged(self, path: str) -> None:
        path = repr(path)
        changed: bool = path != OptionsManager.getDispath()
        self.pendingChanges.emit(OptionKeys.dispath, changed)
    
    @Slot(str)
    def langChanged(self, lang: str) -> None:
        lang = LANG_STR_TO_CODE.get(lang, '')
        changed: bool = lang != OptionsManager.getLang()
        self.pendingChanges.emit(OptionKeys.lang, changed)
    
    @Slot(str)
    def themeChanged(self, theme: str) -> None:
        changed: bool = theme != OptionsManager.getTheme()
        self.pendingChanges.emit(OptionKeys.color_theme, changed)
    
    @Slot()
    def setUpdateAlert(self) -> None:
        changed: bool = self.updateAlertCheckbox.isChecked() != OptionsManager.getMMMUpdateAlert()
        self.pendingChanges.emit(OptionKeys.mmm_update_alert, changed)
    
    def CheckUpdate(self) -> None:
        self.CheckUpdateButton.setText(qapp.translate("OptionsGeneral", 'Checking...'))
        self.run_CheckUpdate.start()