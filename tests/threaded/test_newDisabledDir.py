import os
import shutil
import pytest
from typing import Generator

from PySide6.QtCore import QMutex

from pytestqt.qtbot import QtBot

from src.threaded.newDisabledDir import NewDisabledDir
from src.save import OptionsManager

@pytest.fixture(scope='module')
def create_worker(create_mod_dirs: str, createTemp_Config_ini: str, createTemp_Mod_ini: str) -> Generator:
    newDisabledDir: str = os.path.join(create_mod_dirs, 'newDisabledMods')
    disabledDir: str = os.path.join(create_mod_dirs, 'disabledMods')

    shutil.move(
        os.path.join(create_mod_dirs, 'assets', 'mod_overrides', 'best mod ever'), 
        os.path.join(disabledDir, 'best mod ever')
    )

    mutex = QMutex()
    worker = NewDisabledDir(disabledDir, newDisabledDir)
    worker.mutex = mutex

    yield worker

    worker.deleteLater()

def test_thread(qtbot: QtBot, create_worker: NewDisabledDir) -> None:
    with qtbot.wait_signal(create_worker.succeeded):
        create_worker.start()

    tmp: str = os.path.dirname(OptionsManager.getDispath())

    assert 'best mod ever' in os.listdir(os.path.join(tmp, 'newDisabledMods'))
    assert 'best mod ever' not in os.listdir(OptionsManager.getDispath())

def test_cancel(qtbot: QtBot, create_worker: NewDisabledDir) -> None:
    create_worker.cancel = True
    with qtbot.wait_signal(create_worker.doneCanceling):
        create_worker.cancelCheck()
    
    tmp: str = os.path.dirname(OptionsManager.getDispath())

    assert 'best mod ever' not in os.listdir(os.path.join(tmp, 'newDisabledMods'))
    assert 'best mod ever' in os.listdir(OptionsManager.getDispath())