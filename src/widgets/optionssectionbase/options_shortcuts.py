import PySide6.QtWidgets as qtw
from PySide6.QtCore import QCoreApplication as qapp, Qt
from typing_extensions import override

from src.widgets.optionssectionbase.option_section_base import OptionsSectionBase

class OptionsShortcuts(OptionsSectionBase):
    def __init__(self, parent: qtw.QWidget | None = None) -> None:
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
    
    @override
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