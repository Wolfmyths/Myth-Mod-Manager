import tempfile
import os
from collections.abc import Generator

import pytest
from pytestqt.qtbot import QtBot

import PySide6.QtWidgets as qtw

from src.helpers.options_manager import OptionsManager
from src.widgets.qdialog.gamepath_not_found import GamePathNotFound

MOCK_EXE = 'PAYDAY2.exe'

@pytest.fixture
def create_mockexe() -> Generator[str]:

    with tempfile.TemporaryDirectory() as tmp_dir:
        with open(os.path.join(tmp_dir, MOCK_EXE), 'w'):
            yield tmp_dir

def test_dialog(qtbot: QtBot, createTemp_Config_ini: str, create_mockexe: str) -> None:  # pyright: ignore[reportUnusedParameter]
    widget = GamePathNotFound()
    exe_path = os.path.join(create_mockexe, MOCK_EXE)
    okButton: qtw.QPushButton = widget.buttonBox.button(qtw.QDialogButtonBox.StandardButton.Ok)
    qtbot.addWidget(widget)

    assert okButton.isEnabled() is False

    widget.gameDir.setText(exe_path)

    assert okButton.isEnabled()
    assert not OptionsManager.getGamepath() == create_mockexe
    
    widget.accept()
    assert OptionsManager.getGamepath() == create_mockexe
    assert OptionsManager.getGameExecuteable() == exe_path
