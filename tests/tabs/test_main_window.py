from pytestqt.qtbot import QtBot

import PySide6.QtWidgets as qtw

from src.main_window import MainWindow
from src.constant_vars import PROGRAM_NAME, VERSION

def test_main_window(qtbot: QtBot):
    widget = MainWindow()
    qtbot.addWidget(widget)

    assert not widget.windowIcon().isNull()
    assert widget.windowTitle() == f'{PROGRAM_NAME} {VERSION}'
    assert len(widget.findChildren(qtw.QTabWidget)) == 1
    assert widget.tab.count() == 4
