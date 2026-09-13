import PySide6.QtWidgets as qtw
from PySide6.QtCore import QCoreApplication as qapp, Slot
from typing_extensions import override

from src.widgets.optionssectionbase.option_section_base import OptionsSectionBase
from src.widgets.qlistwidget.ignored_mods import IgnoredMods

class OptionsIgnoredMods(OptionsSectionBase):
    def __init__(self, parent: qtw.QWidget | None = None) -> None:
        super().__init__(parent= parent)

        layout = qtw.QVBoxLayout()

        # Ignored mods list
        self.ignoredModsLabel = qtw.QLabel(self)

        self.ignoredModsListWidget = IgnoredMods(self)
        self.ignoredModsListWidget.itemsChanged.connect(self.updateModIgnoreLabel)

        for widget in (self.ignoredModsLabel, self.ignoredModsListWidget):
            layout.addWidget(widget)
        
        self.setLayout(layout)
    
    @override
    def applyStaticText(self) -> None:
        self.updateModIgnoreLabel()

    @Slot()
    def updateModIgnoreLabel(self) -> None:
        self.ignoredModsLabel.setText(qapp.translate("OptionsIgnoredMods", 'Hidden Mods:') + f' {self.ignoredModsListWidget.count()}')
