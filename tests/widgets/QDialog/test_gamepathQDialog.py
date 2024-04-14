import tempfile
import os
from typing import Generator

import pytest
from pytestqt.qtbot import QtBot

import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt as qt

from src.widgets.QDialog.gamepathQDialog import GamePathNotFound

@pytest.fixture
def create_mockexe() -> Generator:

    with tempfile.TemporaryDirectory() as tmp_dir:
        with open(os.path.join(tmp_dir, 'payday2_win32_release.exe'), 'w'):

            yield tmp_dir

def test_dialog(qtbot: QtBot, createTemp_Config_ini: str, create_mockexe: str) -> None:
    widget = GamePathNotFound(qtw.QWidget(), createTemp_Config_ini)
    okButton = widget.buttonBox.button(qtw.QDialogButtonBox.StandardButton.Ok)
    qtbot.addWidget(widget)

    assert okButton.isEnabled() == False

    widget.gameDir.setText(create_mockexe)

    assert okButton.isEnabled()
    assert widget.optionsManager.getGamepath() != create_mockexe
    
    QtBot.mouseClick(okButton, qt.MouseButton.LeftButton)
    assert widget.optionsManager.getGamepath() == os.path.abspath(create_mockexe)
