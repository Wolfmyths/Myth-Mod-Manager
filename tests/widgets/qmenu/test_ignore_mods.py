from pytestqt.qtbot import QtBot

from src.widgets.qmenu.ignored_mods import IgnoredModsQMenu

def test_menu(qtbot: QtBot) -> None:
    widget = IgnoredModsQMenu()
    qtbot.addWidget(widget)
