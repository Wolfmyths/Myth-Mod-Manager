import os
import pytest
from collections.abc import Generator

from PySide6.QtCore import QMutex

from pytestqt.qtbot import QtBot

from src.objects.move_to_disabled_dir import MoveToDisabledDir
from src.helpers.options_manager import OptionsManager

@pytest.fixture(scope='module')
def create_worker(create_mod_dirs: str, createTemp_Config_ini: str, createTemp_Mod_ini: str) -> Generator[MoveToDisabledDir]:  # pyright: ignore[reportUnusedParameter]
    mutex = QMutex()
    worker = MoveToDisabledDir('make game easy mod')
    worker.mutex = mutex

    yield worker

    worker.deleteLater()

def test_thread(qtbot: QtBot, create_worker: MoveToDisabledDir) -> None:
    with qtbot.wait_signal(create_worker.succeeded):
        create_worker.start()

    assert os.path.exists(os.path.join(OptionsManager.getDispath(), 'make game easy mod'))
    assert not os.path.exists(os.path.join(OptionsManager.getGamepath(), 'mods', 'make game easy mod'))

def test_cancel(qtbot: QtBot, create_worker: MoveToDisabledDir) -> None:
    create_worker.cancel = True
    with qtbot.wait_signal(create_worker.doneCanceling):
        create_worker.cancelCheck()

    assert not os.path.exists(os.path.join(OptionsManager.getDispath(), 'make game easy mod'))
    assert os.path.exists(os.path.join(OptionsManager.getGamepath(), 'mods', 'make game easy mod'))
