import pytest
from pytestqt.qtbot import QtBot

from PySide6.QtCore import Qt as qt

from src.widgets.toolQWidget import ExternalToolDisplay

MOCK_NAME = 'new name'
MOCK_URLS = ('C:\\this\\is\\a\\mock\\url.exe', 'D:\\this\\is\\a\\mock\\url2.bat')

EXPECTED_URL = 'C:\\path\\program.exe'

# ExternalToolDisplay starts with 3 items
@pytest.fixture(scope='function')
def create_ExternalToolDisplay(createTemp_externalShortcuts_ini: str) -> ExternalToolDisplay:
    return ExternalToolDisplay(createTemp_externalShortcuts_ini)

def test_deleteItem(create_ExternalToolDisplay: ExternalToolDisplay) -> None:

    create_ExternalToolDisplay.deleteItem(EXPECTED_URL)

    assert create_ExternalToolDisplay.count() == 2

def test_changeName(create_ExternalToolDisplay: ExternalToolDisplay) -> None:

    create_ExternalToolDisplay.changeName(MOCK_NAME, EXPECTED_URL)

    assert create_ExternalToolDisplay.item(0).text() == MOCK_NAME

def test_addTool(create_ExternalToolDisplay: ExternalToolDisplay) -> None:
    create_ExternalToolDisplay.addTool(*MOCK_URLS, save=False)

    assert create_ExternalToolDisplay.count() == 5
    assert create_ExternalToolDisplay.item(3).text() == MOCK_URLS[0]
    assert create_ExternalToolDisplay.item(4).text() == MOCK_URLS[1]

def test_ExternalToolDisplay(qtbot: QtBot, create_ExternalToolDisplay: ExternalToolDisplay) -> None:

    qtbot.addWidget(create_ExternalToolDisplay)
