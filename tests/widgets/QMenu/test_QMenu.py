from pytestqt.qtbot import QtBot

from PySide6.QtCore import Qt as qt

from src.widgets.qmenu.mod_context_menu import ModContextMenu

def test_menu(qtbot: QtBot) -> None:
    widget = ModContextMenu()
    qtbot.addWidget(widget)
    widget.show()

    qtbot.mouseClick(widget, qt.MouseButton.LeftButton)  # pyright: ignore[reportUnknownMemberType]
    qtbot.mouseRelease(widget, qt.MouseButton.LeftButton)  # pyright: ignore[reportUnknownMemberType]

    assert widget.wasLastClickLMB()

    qtbot.mouseClick(widget, qt.MouseButton.LeftButton)  # pyright: ignore[reportUnknownMemberType]
    qtbot.mouseRelease(widget, qt.MouseButton.RightButton)  # pyright: ignore[reportUnknownMemberType]

    assert not widget.wasLastClickLMB()