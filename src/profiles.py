
import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
from PySide6.QtCore import Qt as qt

from save import OptionsManager, Save

class modProfile(qtw.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.saveManager = Save()
        self.optionsManager = OptionsManager()
