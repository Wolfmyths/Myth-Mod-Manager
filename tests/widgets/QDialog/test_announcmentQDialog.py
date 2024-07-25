from pytestqt.qtbot import QtBot

from src.widgets.QDialog.announcementQDialog import Notice

def test_dialog(qtbot: QtBot) -> None:
    widget = Notice('message', 'headline')
    qtbot.addWidget(widget)

    assert widget.warningLabel.text() == 'message'
    assert widget.windowTitle() == 'headline'
