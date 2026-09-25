import os
from collections.abc import Generator

import pytest
from pytestqt.qtbot import QtBot

from PySide6.QtWidgets import QListWidgetItem

from src.widgets.qlistwidget.external_tool_display import ExternalToolDisplay

NEW_URL = os.path.abspath(
    os.path.join('E:', 'this', 'is', 'a', 'new', 'mock', 'url.exe'))

MOCK_URLS = (
    os.path.abspath(os.path.join('this', 'is', 'a', 'mock', 'url.exe')),
    os.path.abspath(os.path.join('D:', 'this', 'is', 'a', 'mock', 'url2.bat')))

EXPECTED_URL = os.path.abspath(os.path.join('path', 'program.exe'))
URL_TO_BE_DELETED = os.path.abspath(os.path.join('D:', 'path', 'payday.exe'))

# ExternalToolDisplay starts with 3 items
@pytest.fixture(scope='function')
def create_ExternalToolDisplay(createTemp_externalShortcuts_ini: str) -> Generator[ExternalToolDisplay]:  # pyright: ignore[reportUnusedParameter]
    yield ExternalToolDisplay()

def test_deleteItem(create_ExternalToolDisplay: ExternalToolDisplay) -> None:

    create_ExternalToolDisplay.deleteItem(URL_TO_BE_DELETED)

    assert create_ExternalToolDisplay.count() == 2

def test_changeName(create_ExternalToolDisplay: ExternalToolDisplay) -> None:

    create_ExternalToolDisplay.changeName(NEW_URL, EXPECTED_URL)
    item: QListWidgetItem = create_ExternalToolDisplay.item(0)
    assert item.text() == NEW_URL

def test_addTool(create_ExternalToolDisplay: ExternalToolDisplay) -> None:
    create_ExternalToolDisplay.addTool(*MOCK_URLS, save=False)

    assert create_ExternalToolDisplay.count() == 4
    assert create_ExternalToolDisplay.item(2).text() == MOCK_URLS[0]
    assert create_ExternalToolDisplay.item(3).text() == MOCK_URLS[1]

def test_ExternalToolDisplay(qtbot: QtBot, create_ExternalToolDisplay: ExternalToolDisplay) -> None:

    qtbot.addWidget(create_ExternalToolDisplay)
