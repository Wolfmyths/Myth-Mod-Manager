import tempfile
import os
import platform
from collections.abc import Generator

import pytest
from pytestqt.qtbot import QtBot

import PySide6.QtWidgets as qtw

from src.helpers.options_manager import OptionsManager
from src.widgets.qdialog.gamepath_not_found import GamePathNotFound

MOCK_EXE = 'payday2_win32_release.exe' if platform.system().startswith('Win') else 'payday2_release'

@pytest.fixture
def create_mockexe() -> Generator[str]:

    with tempfile.TemporaryDirectory() as tmp_dir:
        with open(os.path.join(tmp_dir, MOCK_EXE), 'w'):

            yield tmp_dir

def test_dialog(qtbot: QtBot, createTemp_Config_ini: str, create_mockexe: str) -> None:  # pyright: ignore[reportUnusedParameter]
    widget = GamePathNotFound(qtw.QWidget())
    okButton: qtw.QPushButton = widget.buttonBox.button(qtw.QDialogButtonBox.StandardButton.Ok)
    qtbot.addWidget(widget)

    assert okButton.isEnabled() is False

    widget.gameDir.setText(create_mockexe)

    assert okButton.isEnabled()
    assert OptionsManager.getGamepath() != create_mockexe
    
    widget.accept()
    assert OptionsManager.getGamepath() == os.path.abspath(create_mockexe)
