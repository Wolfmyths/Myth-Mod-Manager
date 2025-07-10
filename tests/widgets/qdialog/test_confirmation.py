from pytestqt.qtbot import QtBot

from src.widgets.qdialog.confirmation import Confirmation

def test_dialog(qtbot: QtBot) -> None:
    widget = Confirmation('title', 'body')
    qtbot.addWidget(widget)
