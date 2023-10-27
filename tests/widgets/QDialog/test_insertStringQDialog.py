from pytestqt.qtbot import QtBot

from src.widgets.QDialog.insertStringQDialog import insertString

def test_dialog(qtbot: QtBot) -> None:
    widget = insertString('prompt')
    qtbot.addWidget(widget)

    assert widget.label.text() == 'prompt'

    widget.inputString.setText('test')

    widget.buttonBox.accepted.emit()

    assert widget.userInput == 'test'
    assert widget.result() == 1
