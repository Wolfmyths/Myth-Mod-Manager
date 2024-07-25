from pytestqt.qtbot import QtBot

from PySide6.QtCore import Qt as qt

from src.widgets.QDialog.tagHandlerQDialog import TagHandler

MOCK_ALL_TAGS = ['anime', 'favorites', 'joke']

def test_tagHandler(qtbot: QtBot) -> None:
    widget = TagHandler(0, MOCK_ALL_TAGS)
    qtbot.addWidget(widget)

def test_lineEditTextChanged(qtbot: QtBot) -> None:
    widget = TagHandler(0, MOCK_ALL_TAGS)

    qtbot.addWidget(widget)

    qtbot.mouseClick(widget.input, qt.MouseButton.LeftButton)
    qtbot.keyClick(widget.input, qt.Key.Key_A)
    assert widget.completer.completionPrefix() == 'a'

    assert widget.buttonBox.buttons()[0].isEnabled()
