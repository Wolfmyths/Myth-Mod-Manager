from pytestqt.qtbot import QtBot

from src.widgets.QMenu.managerQMenu import ManagerMenu
from src.widgets.managerQTableWidget import ModListWidget

def test_menu(qtbot: QtBot) -> None:
    widget = ManagerMenu(ModListWidget())
    qtbot.addWidget(widget)
