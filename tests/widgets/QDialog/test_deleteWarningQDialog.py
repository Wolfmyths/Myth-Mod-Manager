from pytestqt.qtbot import QtBot

from src.widgets.QDialog.deleteWarningQDialog import DeleteModConfirmation

def test_dialog(qtbot: QtBot) -> None:
    widget = DeleteModConfirmation()
    qtbot.addWidget(widget)
