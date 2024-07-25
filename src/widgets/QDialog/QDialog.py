
import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
from PySide6.QtCore import Qt as qt

from src.constant_vars import ICON

class Dialog(qtw.QDialog):
    '''This is the qtw.QDialog Base Class for Myth Mod Manager'''
    def __init__(self) -> None:
        super().__init__()

        self.setWindowIcon(qtg.QIcon(ICON))
        self.setWindowFlag(qt.WindowType.WindowStaysOnTopHint, True)