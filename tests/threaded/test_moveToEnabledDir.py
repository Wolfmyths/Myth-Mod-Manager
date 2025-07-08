import os
import shutil
import pytest
from typing import Generator

from PySide6.QtCore import QMutex

from pytestqt.qtbot import QtBot

from src.threaded.moveToEnabledDir import MoveToEnabledModDir
from src.save import OptionsManager

@pytest.fixture(scope='module')
def create_worker(create_mod_dirs: str, createTemp_Config_ini: str, createTemp_Mod_ini: str) -> Generator:
    enabledDir: str = os.path.join(create_mod_dirs, 'mods', 'make game easy mod')
    disabledDir: str = os.path.join(create_mod_dirs, 'disabledMods', 'make game easy mod')

    shutil.move(enabledDir, disabledDir)

    mutex = QMutex()
    worker = MoveToEnabledModDir('make game easy mod')
    worker.mutex = mutex

    yield worker

    worker.deleteLater()

def test_thread(qtbot: QtBot, create_worker: MoveToEnabledModDir) -> None:
    with qtbot.wait_signal(create_worker.succeeded):
        create_worker.start()

    assert os.path.exists(os.path.join(OptionsManager.getGamepath(), 'mods', 'make game easy mod'))
    assert not os.path.exists(os.path.join(OptionsManager.getDispath(), 'disabledMods', 'make game easy mod'))

def test_cancel(qtbot: QtBot, create_worker: MoveToEnabledModDir) -> None:
    create_worker.cancel = True
    with qtbot.wait_signal(create_worker.doneCanceling):
        create_worker.cancelCheck()
    
    assert 'make game easy mod' not in os.listdir(os.path.join(OptionsManager.getGamepath(), 'mods'))
    assert 'make game easy mod' in os.listdir(OptionsManager.getDispath())

