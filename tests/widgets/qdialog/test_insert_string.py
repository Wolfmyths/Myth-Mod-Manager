from pytestqt.qtbot import QtBot

from src.widgets.qdialog.insert_string import InsertString

def test_dialog(qtbot: QtBot) -> None:
    widget = InsertString('prompt')
    qtbot.addWidget(widget)

    assert widget.label.text() == 'prompt'

    widget.inputString.setText('test')

    widget.buttonBox.accepted.emit()

    assert widget.userInput == 'test'
    assert widget.result() == 1
