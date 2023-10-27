import tempfile
import os

import pytest
from pytestqt.qtbot import QtBot

import PySide6.QtWidgets as qtw

from src.widgets.QDialog.gamepathQDialog import GamePathNotFound


@pytest.fixture
def create_mockexe() -> str:

    with tempfile.TemporaryDirectory() as tmp_dir:
        with open(os.path.join(tmp_dir, 'payday2_win32_release.exe'), 'w'):

            yield tmp_dir

def test_dialog(qtbot: QtBot, createTemp_Config_ini: str, create_mockexe: str) -> None:
    widget = GamePathNotFound(qtw.QWidget(), createTemp_Config_ini)
    qtbot.addWidget(widget)

    widget.gameDir.setText('gamedir')

    assert widget.buttonBox.button(qtw.QDialogButtonBox.StandardButton.Ok).isEnabled() == False
    assert widget.optionsManager.getGamepath() != 'gamedir'

    widget.gameDir.setText(create_mockexe)

    assert widget.buttonBox.button(qtw.QDialogButtonBox.StandardButton.Ok).isEnabled()
    assert widget.optionsManager.getGamepath() == create_mockexe

    
