from pytestqt.qtbot import QtBot

from src.widgets.QMenu.profileQMenu import ProfileMenu
from src.widgets.modProfileQTreeWidget import ProfileList

def test_menu(qtbot: QtBot) -> None:
    widget = ProfileMenu(ProfileList())
    qtbot.addWidget(widget)
