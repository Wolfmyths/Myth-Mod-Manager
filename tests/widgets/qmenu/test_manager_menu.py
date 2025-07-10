from pytestqt.qtbot import QtBot

from src.widgets.qmenu.manager_menu import ManagerMenu
from src.widgets.qtable.mod_list_widget import ModListWidget

def test_menu(qtbot: QtBot) -> None:
    widget = ManagerMenu(ModListWidget())
    qtbot.addWidget(widget)
