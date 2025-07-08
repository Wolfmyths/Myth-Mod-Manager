import os
import logging
import sys

import PySide6.QtWidgets as qtw
from PySide6.QtCore import QCoreApplication as qapp, Signal, Qt, QTranslator, Slot

from src.widgets.progressWidget import ProgressWidget
from src.threaded.backupMods import BackupMods
from src.threaded.newDisabledDir import NewDisabledDir
from src.save import OptionsManager
from src.getPath import Pathing
from src.style import StyleManager
from src.widgets.ignoredModsQListWidget import IgnoredMods
from src.constant_vars import DARK, LIGHT, ROOT_PATH, OptionKeys, LANG_FOLDER_PATH
from src.widgets.QDialog.newUpdateQDialog import updateDetected
from src.widgets.QDialog.announcementQDialog import Notice

from src.api.checkUpdate import checkUpdate

from src import errorChecking

language_string_to_code: dict[str:str] = {
    'Deutsch'            : 'de_DE',
    'English'            : 'en_US',
    'Español (españa)'   : 'es_ES',
    'Français'           : 'fr_FR',
    'Italiano'           : 'it_IT',
    '日本語'              : 'ja_JP',
    '한국인'              : 'ko_KR',
    'Nederlands'         : 'nl_NL',
    'Polski'             : 'pl_PL',
    'Português (Brasil)' : 'pt_BR',
    'Русский'            : 'ru_RU',
    '中文（简体）'        : 'zh_CN'
}

language_code_to_string: dict = {x:y for y,x in language_string_to_code.items()}

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
        self.optionsMisc = OptionsMisc(self)

        self.sections: dict[str: qtw.QWidget] = {
            'General'      : self.optionsGeneral,
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

        for widget in (self.sectionsList, self.sectionsDisplay):
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
        for widget in tuple(self.sections.values()):
            widget: OptionsSectionBase
            widget.pendingChanges.connect(self.settingsChanged)
    
    @Slot(qtw.QListWidgetItem)
    def onSectionsListItemClicked(self, item: qtw.QListWidgetItem) -> None:
        self.sectionsDisplay.setCurrentIndex(self.sectionsList.row(item))

    def applyStaticText(self) -> None:
        self.applyButton.setText(qapp.translate('Options', 'Apply'))
        self.cancelButton.setText(qapp.translate('Options', 'Cancel'))

        self.sectionsList.item(0).setText(qapp.translate('Options', 'General'))
        self.sectionsList.item(1).setText(qapp.translate('Options', 'Ignored Mods'))
        self.sectionsList.item(2).setText(qapp.translate('Options', 'Shortcuts'))
        self.sectionsList.item(3).setText(qapp.translate('Options', 'Misc'))

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
            OptionsManager.setGamepath(self.optionsGeneral.gameDir.text())

        if self.optionChanged.get(OptionKeys.dispath):
            old_path: str = OptionsManager.getDispath()
            new_path: str = self.optionsGeneral.disabledModDir.text()

            is_dir: bool = os.path.isdir(new_path)
            is_abs: bool = os.path.isabs(new_path)
            is_valid: bool = is_dir and is_abs

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
                is_dir,
                is_abs
            )

        if self.optionChanged.get(OptionKeys.color_theme):
            theme = LIGHT if self.optionsGeneral.colorThemeLight.isChecked() else DARK
            OptionsManager.setTheme(theme)

            app: qtw.QApplication = qtw.QApplication.instance()
            app.setStyleSheet(StyleManager().getStyleSheet(theme))

            self.themeSwitched.emit(theme)

        if self.optionChanged.get(OptionKeys.mmm_update_alert):
            OptionsManager.setMMMUpdateAlert(self.optionsGeneral.updateAlertCheckbox.isChecked())
        
        if self.optionChanged.get(OptionKeys.lang):
            app: qtw.QApplication = qtw.QApplication.instance()

            old_lang: str = OptionsManager.getLang()
            new_lang: str | None = language_string_to_code.get(self.optionsGeneral.language.currentText())

            translator: QTranslator = app.findChild(QTranslator)

            if translator.load(os.path.join(LANG_FOLDER_PATH, new_lang + '.qm')):
                OptionsManager.setLang(new_lang)

                logging.info('Changed lang from %s to %s', old_lang, new_lang)
            else:
                logging.error('Loading lang %s failed', new_lang)

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
            self.optionsGeneral.language.setCurrentText(language_code_to_string.get(OptionsManager.getLang()))

        self.resetPendingOptions()

        self.applyButton.setEnabled(False)
        self.cancelButton.setEnabled(False)

class OptionsSectionBase(qtw.QWidget):
    pendingChanges = Signal(OptionKeys, bool)

    def __init__(self, parent: Options = None) -> None:
        super().__init__(parent=parent)

    def applyStaticText(self) -> None:
        return

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
        self.language.addItems(list(language_string_to_code.keys()))
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

        self.checkUpdateButton = qtw.QPushButton(self)
        self.checkUpdateButton.clicked.connect(self.checkUpdate)

        for widget in (self.updateAlertCheckbox, self.checkUpdateButton):
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
        self.checkUpdateButton.setText(qapp.translate("OptionsGeneral", "Check for updates"))

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
        lang = language_string_to_code.get(lang)
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
    
    def checkUpdate(self) -> None:
        @Slot(str, str)
        def updateFound(latestVersion: str, changelog: str) -> None:
            notice = updateDetected(latestVersion, changelog)
            notice.rejected.connect(lambda: self.checkUpdateButton.setText(qapp.translate("OptionsGeneral", 'Check for updates')))
            notice.exec()
            
            if notice.result():
                errorChecking.startFile(os.path.join(ROOT_PATH, 'Myth Mod Manager.exe'))
                qapp.quit()

        self.checkUpdateButton.setText(qapp.translate("OptionsGeneral", 'Checking...'))

        self.run_checkupdate = checkUpdate()
        self.run_checkupdate.updateDetected.connect(updateFound)
        self.run_checkupdate.error.connect(lambda: self.checkUpdateButton.setText(qapp.translate("OptionsGeneral", 'Error: Check logs for more info')))
        self.run_checkupdate.upToDate.connect(lambda: self.checkUpdateButton.setText(qapp.translate("OptionsGeneral", 'Up to date!' ) + ' ^_^' ))

class OptionsIgnoredMods(OptionsSectionBase):
    def __init__(self, parent: Options = None) -> None:
        super().__init__(parent= parent)

        layout = qtw.QVBoxLayout()

        # Ignored mods list
        self.ignoredModsLabel = qtw.QLabel(self)

        self.ignoredModsListWidget = IgnoredMods(self)
        self.ignoredModsListWidget.itemsChanged.connect(self.updateModIgnoreLabel)

        for widget in (self.ignoredModsLabel, self.ignoredModsListWidget):
            layout.addWidget(widget)
        
        self.setLayout(layout)
    
    @Slot()
    def updateModIgnoreLabel(self) -> None:
        self.ignoredModsLabel.setText(qapp.translate("OptionsIgnoredMods", 'Hidden Mods:') + f' {self.ignoredModsListWidget.count()}')

class OptionsShortcuts(OptionsSectionBase):
    def __init__(self, parent: Options = None) -> None:
        super().__init__(parent= parent)

        layout = qtw.QVBoxLayout()

        self.gbShortcuts = qtw.QGroupBox(self)

        gbShortcutsLayout = qtw.QVBoxLayout()

        self.shortcutsLabel = qtw.QLabel(self)

        self.shortcutsLabel.setTextFormat(Qt.TextFormat.MarkdownText)
        gbShortcutsLayout.addWidget(self.shortcutsLabel)
        self.gbShortcuts.setLayout(gbShortcutsLayout)

        layout.addWidget(self.gbShortcuts)

        self.applyStaticText()

        self.setLayout(layout)
    
    def applyStaticText(self) -> None:
        self.gbShortcuts.setTitle(qapp.translate("OptionsShortcuts", "Shortcuts"))

        self.shortcutsLabel.setText(
            '\n\n'.join([
                '+ ' + qapp.translate("OptionsShortcuts", 'Select All:') + ' Ctrl + A',
                '+ ' + qapp.translate("OptionsShortcuts", 'Deselect All:') + ' Ctrl + D',
                '+ ' + qapp.translate("OptionsShortcuts", 'Delete Mod or Profile:') + ' Del',
                '+ ' + qapp.translate("OptionsShortcuts", 'Change Profile Name:') + ' Enter',
                '+ ' + qapp.translate("OptionsShortcuts", 'Switch tabs: Arrow left, Arrow right')
        ]))

class OptionsMisc(OptionsSectionBase):
    def __init__(self, parent: Options = None) -> None:
        super().__init__(parent= parent)

        layout = qtw.QVBoxLayout()
        
        self.miscGroup = qtw.QGroupBox(self)

        miscGroupLayout = qtw.QVBoxLayout()

        self.backupMods = qtw.QPushButton(self)
        self.backupMods.clicked.connect(self.startBackupMods)

        self.log = qtw.QPushButton(self)
        self.log.clicked.connect(self.openCrashLogs)

        self.modLog = qtw.QPushButton(self)
        self.modLog.clicked.connect(self.openCrashLogBLT)

        for widget in (self.backupMods, self.log, self.modLog):
            miscGroupLayout.addWidget(widget)
        
        self.miscGroup.setLayout(miscGroupLayout)

        for widget in (self.miscGroup, ):
            layout.addWidget(widget)

        self.applyStaticText()

        self.setLayout(layout)
    
    def applyStaticText(self) -> None:
        self.miscGroup.setTitle(qapp.translate("OptionsMisc", "Misc"))

        self.backupMods.setText(qapp.translate("OptionsMisc", "Backup Mods"))
        self.backupMods.setToolTip(qapp.translate("OptionsMisc", "Copies and compresses all of your mods to MMM's installation folder"))

        self.log.setText(qapp.translate("OptionsMisc", "Open Crash Logs..."))
        self.log.setToolTip(qapp.translate("OptionsMisc", "Opens the crash log directory used by vanilla Payday 2"))

        self.modLog.setText(qapp.translate("OptionsMisc", "Open Mod Crash Logs..."))
        self.modLog.setToolTip(qapp.translate("OptionsMisc", "Opens the crash log directory that BLT uses"))
    
    @Slot()
    def openCrashLogBLT(self) -> None:
        modPath: str = Pathing.mods()

        errorChecking.startFile(os.path.join(modPath, 'logs'))
    
    @Slot()
    def openCrashLogs(self) -> None:

        if sys.platform.startswith('win'):
            os.startfile(os.path.join('C:', 'Users', os.environ['USERNAME'], 'AppData', 'Local', 'PAYDAY 2'))
        else:
            notice = Notice(
                qapp.translate("OptionsMisc", 'Overkill did not implement a vanilla crash log for linux') + ' :(',
                qapp.translate("OptionsMisc", 'Myth Mod Manager: Vanilla crash logs unsupported')
            )
            notice.exec()
    
    @Slot()
    def startBackupMods(self) -> None:
        
        startFileMover = ProgressWidget(BackupMods())
        startFileMover.exec()
