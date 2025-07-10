from pytestqt.qtbot import QtBot

from src.widgets.qdialog.dialog import Dialog

def test_dialog(qtbot: QtBot) -> None:
    widget = Dialog()
    qtbot.addWidget(widget)
