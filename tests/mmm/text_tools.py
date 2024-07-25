from pytestqt.qtbot import QtBot

from src.tools import ToolManager

def test_ToolManager(qtbot: QtBot):
    widget = ToolManager()

    qtbot.addWidget(widget)
