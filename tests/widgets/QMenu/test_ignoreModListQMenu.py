from pytestqt.qtbot import QtBot

from src.widgets.QMenu.ignoreModListQMenu import IgnoredModsQMenu

def test_menu(qtbot: QtBot) -> None:
    widget = IgnoredModsQMenu()
    qtbot.addWidget(widget)
