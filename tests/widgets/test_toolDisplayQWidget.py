from pytestqt.qtbot import QtBot

from src.widgets.toolDisplayQWidget import ExternalTool

MOCK_URL = 'C:\\path\\program.exe'

def test_ExternalTool(qtbot: QtBot) -> None:

    widget = ExternalTool(MOCK_URL)

    qtbot.addWidget(widget)

    assert widget.toolURL == MOCK_URL
    assert widget.startToolButton.text() == 'program'
