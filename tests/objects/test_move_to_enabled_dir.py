import os
import shutil
import pytest
from collections.abc import Generator

from pytestqt.qtbot import QtBot

from src.objects.move_to_enabled_dir import MoveToEnabledModDir
from src.helpers.options_manager import OptionsManager

@pytest.fixture(scope='module')
def movetoenabledmoddir(create_mod_dirs: str, createTemp_Config_ini: str, createTemp_Mod_ini: str) -> Generator[MoveToEnabledModDir]:  # pyright: ignore[reportUnusedParameter]
    enabledDir: str = os.path.join(create_mod_dirs, 'mods', 'make game easy mod')
    disabledDir: str = os.path.join(create_mod_dirs, 'disabledMods', 'make game easy mod')

    shutil.move(enabledDir, disabledDir)

    worker = MoveToEnabledModDir('make game easy mod')

    yield worker

    worker.deleteLater()

def test_thread(qtbot: QtBot, movetoenabledmoddir: MoveToEnabledModDir) -> None:
    with qtbot.wait_signal(movetoenabledmoddir.succeeded, timeout=500):
        movetoenabledmoddir.start()

    assert os.path.exists(os.path.join(OptionsManager.getGamepath(), 'mods', 'make game easy mod'))
    assert not os.path.exists(os.path.join(OptionsManager.getDispath(), 'disabledMods', 'make game easy mod'))

def test_cancel(qtbot: QtBot, movetoenabledmoddir: MoveToEnabledModDir) -> None:
    movetoenabledmoddir.cancel = True
    with qtbot.wait_signal(movetoenabledmoddir.doneCanceling, timeout=500):
        movetoenabledmoddir.cancelCheck()
    
    assert 'make game easy mod' not in os.listdir(os.path.join(OptionsManager.getGamepath(), 'mods'))
    assert 'make game easy mod' in os.listdir(OptionsManager.getDispath())

