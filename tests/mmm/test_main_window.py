from pytestqt.qtbot import QtBot

import PySide6.QtWidgets as qtw
from PySide6.QtCore import QSize

from src.main_window import MainWindow
from src.constant_vars import PROGRAM_NAME, VERSION

def test_main_window(qtbot: QtBot, createTemp_Config_ini: str, createTemp_Mod_ini: str) -> None:
    widget = MainWindow(optionsPath=createTemp_Config_ini, savePath=createTemp_Mod_ini)
    qtbot.addWidget(widget)

    assert not widget.windowIcon().isNull()                          # Has icon
    assert widget.windowTitle() == f'{PROGRAM_NAME} {VERSION}'       # Window has title
    assert len(widget.findChildren(qtw.QTabWidget)) == 1             # Has a tab widget
    assert widget.tab.count() == 4                                   # Amount of tabs

    widget.resize(1000, 900)
    widget.close()
    assert widget.optionsManager.getWindowSize() == QSize(1000, 900) # Saving window size
