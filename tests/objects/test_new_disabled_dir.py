import os
import shutil
import pytest
from collections.abc import Generator

from pytestqt.qtbot import QtBot

from src.objects.new_disabled_dir import NewDisabledDir
from src.helpers.options_manager import OptionsManager

@pytest.fixture(scope='module')
def newdisableddir(create_mod_dirs: str, createTemp_Config_ini: str, createTemp_Mod_ini: str) -> Generator[NewDisabledDir]:  # pyright: ignore[reportUnusedParameter]
    newDisabledDir: str = os.path.join(create_mod_dirs, 'newDisabledMods')
    disabledDir: str = os.path.join(create_mod_dirs, 'disabledMods')

    shutil.move(
        os.path.join(create_mod_dirs, 'assets', 'mod_overrides', 'best mod ever'), 
        os.path.join(disabledDir, 'best mod ever')
    )

    worker = NewDisabledDir(disabledDir, newDisabledDir)

    yield worker

    worker.deleteLater()

def test_newdisableddir(qtbot: QtBot, newdisableddir: NewDisabledDir) -> None:
    with qtbot.wait_signal(newdisableddir.succeeded, timeout=500):
        newdisableddir.start()

    tmp: str = os.path.dirname(OptionsManager.getDispath())

    assert 'best mod ever' in os.listdir(os.path.join(tmp, 'newDisabledMods'))
    assert 'best mod ever' not in os.listdir(OptionsManager.getDispath())

def test_newdisableddir_cancel(qtbot: QtBot, newdisableddir: NewDisabledDir) -> None:
    newdisableddir.cancel = True
    with qtbot.wait_signal(newdisableddir.doneCanceling, timeout=500):
        newdisableddir.cancelCheck()
    
    tmp: str = os.path.dirname(OptionsManager.getDispath())

    assert 'best mod ever' not in os.listdir(os.path.join(tmp, 'newDisabledMods'))
    assert 'best mod ever' in os.listdir(OptionsManager.getDispath())