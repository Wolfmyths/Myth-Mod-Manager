from pytestqt.qtbot import QtBot

from src.widgets.QDialog.deleteWarningQDialog import Confirmation

def test_dialog(qtbot: QtBot) -> None:
    widget = Confirmation('title', 'body')
    qtbot.addWidget(widget)
