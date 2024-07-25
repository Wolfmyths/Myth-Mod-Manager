from pytestqt.qtbot import QtBot

from src.widgets.QDialog.QDialog import Dialog

def test_dialog(qtbot: QtBot) -> None:
    widget = Dialog()
    qtbot.addWidget(widget)
