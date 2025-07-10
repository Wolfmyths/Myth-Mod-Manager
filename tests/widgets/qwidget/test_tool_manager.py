from pytestqt.qtbot import QtBot

from src.widgets.qwidget.tool_manager import ToolManager

def test_ToolManager(qtbot: QtBot) -> None:
    widget = ToolManager()

    qtbot.addWidget(widget)
