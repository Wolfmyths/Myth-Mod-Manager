from pytestqt.qtbot import QtBot

from PySide6.QtCore import Qt as qt

from src.widgets.QMenu.QMenu import ModContextMenu

def test_menu(qtbot: QtBot) -> None:
    widget = ModContextMenu()
    qtbot.addWidget(widget)
    widget.show()

    qtbot.mouseClick(widget, qt.MouseButton.LeftButton)
    qtbot.mouseRelease(widget, qt.MouseButton.LeftButton)

    assert widget.wasLastClickLMB()

    qtbot.mouseClick(widget, qt.MouseButton.LeftButton)
    qtbot.mouseRelease(widget, qt.MouseButton.RightButton)

    assert not widget.wasLastClickLMB()