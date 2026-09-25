from pytestqt.qtbot import QtBot

from src.widgets.qmenu.profile_menu import ProfileMenu
from src.widgets.qtreewidget.profile_list import ProfileList

def test_menu(qtbot: QtBot) -> None:
    widget = ProfileMenu(ProfileList())
    qtbot.addWidget(widget)
