import os
import logging
from typing import Any, cast

import PySide6.QtWidgets as qtw
from PySide6.QtCore import QCoreApplication as qapp, Signal, Qt, QTranslator, Slot, QFileInfo

from src.widgets.qdialog.progress_widget import ProgressWidget
from src.objects.new_disabled_dir import NewDisabledDir
from src.helpers.options_manager import OptionsManager
from src.helpers.style import StyleManager
from src.constant_vars import DARK, LIGHT, OptionKeys, LANG_FOLDER_PATH, LANG_CODE_TO_STR, LANG_STR_TO_CODE 
from src.widgets.qdialog.notice import Notice
from src.widgets.optionssectionbase.options_general import OptionsGeneral
from src.widgets.optionssectionbase.options_ignored_mods import OptionsIgnoredMods
from src.widgets.optionssectionbase.options_shortcuts import OptionsShortcuts
from src.widgets.optionssectionbase.options_launch_params import OptionsLaunchParams
from src.widgets.optionssectionbase.options_misc import OptionsMisc
from src.widgets.optionssectionbase.option_section_base import OptionsSectionBase

class Options(qtw.QWidget):
    themeSwitched = Signal(str)
    def __init__(self) -> None:
        super().__init__()

        logging.getLogger(__file__)

        layout = qtw.QVBoxLayout()

        # Centeral widget
        self.centeralWidget = qtw.QWidget()

        centeralLayout = qtw.QHBoxLayout()

        self.optionsGeneral = OptionsGeneral(self)
        self.ignoredMods = OptionsIgnoredMods(self)
        self.shortcuts = OptionsShortcuts(self)
        self.launchparams = OptionsLaunchParams(self)
        self.optionsMisc = OptionsMisc(self)

        self.sections: dict[str, qtw.QWidget] = {
            'General'      : self.optionsGeneral,
            'Launch Params': self.launchparams,
            'Ignored Mods' : self.ignoredMods,
            'Shortcuts'    : self.shortcuts,
            'Misc'         : self.optionsMisc
        }

        self.optionChanged: dict[str, bool] = {k:False for k in OptionKeys.all_keys()}

        sectionKeys = list(self.sections.keys())

        # List of sections
        self.sectionsList = qtw.QListWidget()
        self.sectionsList.itemClicked.connect(self.onSectionsListItemClicked)
        self.sectionsList.setSizePolicy(qtw.QSizePolicy.Policy.Minimum, qtw.QSizePolicy.Policy.Preferred)
        self.sectionsList.setSelectionMode(qtw.QListWidget.SelectionMode.SingleSelection)
        self.sectionsList.addItems(sectionKeys)
        self.sectionsList.item(0).setSelected(True)

        # Stacked Widget
        self.sectionsDisplay = qtw.QStackedWidget()

        for key in sectionKeys:
            self.sectionsDisplay.addWidget(self.sections[key])

        self.sectionsDisplay.setCurrentIndex(0)

        for widget in tuple[Any, ...]((self.sectionsList, self.sectionsDisplay)):
            centeralLayout.addWidget(widget)

        self.centeralWidget.setLayout(centeralLayout)

        # Buttons widget
        self.buttonsWidget = qtw.QWidget()

        buttonWidgetLayout = qtw.QHBoxLayout()
        buttonWidgetLayout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.applyButton = qtw.QPushButton(self)
        self.applyButton.setSizePolicy(qtw.QSizePolicy.Policy.Minimum, qtw.QSizePolicy.Policy.Preferred)
        self.applyButton.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.applyButton.setMinimumWidth(100)
        self.applyButton.setEnabled(False)
        self.applyButton.clicked.connect(self.applySettings)

        self.cancelButton = qtw.QPushButton(self)
        self.cancelButton.setSizePolicy(qtw.QSizePolicy.Policy.Minimum, qtw.QSizePolicy.Policy.Preferred)
        self.cancelButton.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.cancelButton.setMinimumWidth(100)
        self.cancelButton.setEnabled(False)
        self.cancelButton.clicked.connect(self.cancelChanges)

        for widget in (self.cancelButton, self.applyButton):
            buttonWidgetLayout.addWidget(widget)

        self.buttonsWidget.setLayout(buttonWidgetLayout)

        for widget in (self.centeralWidget, self.buttonsWidget):
            layout.addWidget(widget)

        self.setLayout(layout)

        self.applyStaticText()

        # Setting all options to show what they're currently set to
        self.cancelChanges(reset=True)

        # Events
        for widget in tuple[qtw.QWidget, ...](self.sections.values()):
            widget = cast(OptionsSectionBase, widget)
            widget.pendingChanges.connect(self.settingsChanged)
    
    @Slot(qtw.QListWidgetItem)
    def onSectionsListItemClicked(self, item: qtw.QListWidgetItem) -> None:
        self.sectionsDisplay.setCurrentIndex(self.sectionsList.row(item))

    def applyStaticText(self) -> None:
        self.applyButton.setText(qapp.translate('Options', 'Apply'))
        self.cancelButton.setText(qapp.translate('Options', 'Cancel'))

        self.sectionsList.item(0).setText(qapp.translate('Options', 'General'))
        self.sectionsList.item(1).setText(qapp.translate('Options', 'Launch Params'))
        self.sectionsList.item(2).setText(qapp.translate('Options', 'Ignored Mods'))
        self.sectionsList.item(3).setText(qapp.translate('Options', 'Shortcuts'))
        self.sectionsList.item(4).setText(qapp.translate('Options', 'Misc'))

    @Slot(str, bool)
    def settingsChanged(self, key: OptionKeys, value: bool) -> None:
        self.optionChanged[key] = value

        # Adds the bools to check if there are any changes
        if sum(list(self.optionChanged.values())):
            self.applyButton.setEnabled(True)
            self.cancelButton.setEnabled(True)

        else:
            self.applyButton.setEnabled(False)
            self.cancelButton.setEnabled(False)

    def resetPendingOptions(self) -> None:
        for k in list(self.optionChanged.keys()):
            self.optionChanged[k] = False

    @Slot()
    def applySettings(self) -> None:
        if self.optionChanged.get(OptionKeys.game_path):
            OptionsManager.setGameExecuteable(self.optionsGeneral.gameDir.text())

        if self.optionChanged.get(OptionKeys.dispath):
            old_path: str = OptionsManager.getDispath()
            new_path: str = self.optionsGeneral.disabledModDir.text()

            file_info = QFileInfo(new_path)

            is_exe: bool = file_info.isExecutable()
            is_abs: bool = file_info.isAbsolute()
            is_valid: bool = is_exe and is_abs

            progressWidget = ProgressWidget(NewDisabledDir(old_path, new_path))

            if is_valid:
                progressWidget.exec()
            else:
                progressWidget.mode.cancel = True
                errmsg: str = qapp.translate(
                    'Options',
                    'Something went wrong applying new disabled mods folder, check logs for more details after closing this window'
                )

                Notice(
                    errmsg,
                    qapp.translate('Options', 'Could not change disabled mods folder')
                ).exec()

            if not progressWidget.mode.cancel:
                OptionsManager.setDispath(new_path)
            else:
                # Revert text
                self.optionsGeneral.disabledModDir.setText(old_path)
            
            logging.info(
                'Changing disabled mods folder from %s to %s\nIs it a directory? %s\n Is it an absolute path? %s',
                old_path,
                new_path,
                is_exe,
                is_abs
            )

        if self.optionChanged.get(OptionKeys.color_theme):
            theme = LIGHT if self.optionsGeneral.colorThemeLight.isChecked() else DARK
            OptionsManager.setTheme(theme)

            qtw.QApplication.setStyle(StyleManager().getStyleSheet(theme))

            self.themeSwitched.emit(theme)

        if self.optionChanged.get(OptionKeys.mmm_update_alert):
            OptionsManager.setMMMUpdateAlert(self.optionsGeneral.updateAlertCheckbox.isChecked())
        
        if self.optionChanged.get(OptionKeys.lang):
            app: qapp | None = qtw.QApplication.instance()

            old_lang: str = OptionsManager.getLang()
            new_lang: str = LANG_STR_TO_CODE.get(self.optionsGeneral.language.currentText(), '')

            translator: QTranslator | None = app.findChild(QTranslator)

            if translator.load(os.path.join(LANG_FOLDER_PATH, new_lang + '.qm')):
                OptionsManager.setLang(new_lang)

                logging.info('Changed lang from %s to %s', old_lang, new_lang)
            else:
                logging.error('Loading lang %s failed', new_lang)
        
        if self.optionChanged.get(OptionKeys.launch_parameters):
            OptionsManager.setLaunchParameters(self.launchparams.previewLineEdit.text())

        self.resetPendingOptions()

        self.applyButton.setEnabled(False)
        self.cancelButton.setEnabled(False)

        OptionsManager.writeData()

    @Slot()
    @Slot(bool)
    def cancelChanges(self, reset: bool = False) -> None:
        '''
        Resets any pending changes if that option has a pending change.
        
        Reset bool will reset pending changes reguardless if the option
        has a pending change.
        '''
        if self.optionChanged.get(OptionKeys.game_path) or reset:
            self.optionsGeneral.gameDir.setText(OptionsManager.getGamepath())

        if self.optionChanged.get(OptionKeys.dispath) or reset:
            self.optionsGeneral.disabledModDir.setText(OptionsManager.getDispath())

        if self.optionChanged.get(OptionKeys.color_theme) or reset:
            if OptionsManager.getTheme() == LIGHT:
                self.optionsGeneral.colorThemeLight.setChecked(True)
            else:
                self.optionsGeneral.colorThemeDark.setChecked(True)

        if self.optionChanged.get(OptionKeys.mmm_update_alert) or reset:
            self.optionsGeneral.updateAlertCheckbox.setChecked(OptionsManager.getMMMUpdateAlert())

        if self.optionChanged.get(OptionKeys.lang) or reset:
            self.optionsGeneral.language.setCurrentText(LANG_CODE_TO_STR.get(OptionsManager.getLang(), ''))

        if self.optionChanged.get(OptionKeys.launch_parameters) or reset:
            self.launchparams.setup()

        self.resetPendingOptions()

        self.applyButton.setEnabled(False)
        self.cancelButton.setEnabled(False)
