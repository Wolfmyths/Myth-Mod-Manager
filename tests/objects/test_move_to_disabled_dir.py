import os
import pytest
from collections.abc import Generator

from pytestqt.qtbot import QtBot

from src.objects.move_to_disabled_dir import MoveToDisabledDir
from src.helpers.options_manager import OptionsManager

@pytest.fixture(scope='module')
def movetodisableddir(create_mod_dirs: str, createTemp_Config_ini: str, createTemp_Mod_ini: str) -> Generator[MoveToDisabledDir]:  # pyright: ignore[reportUnusedParameter]
    worker = MoveToDisabledDir('make game easy mod')

    yield worker

    worker.deleteLater()

def test_movetodisableddir(qtbot: QtBot, movetodisableddir: MoveToDisabledDir) -> None:
    with qtbot.wait_signal(movetodisableddir.succeeded, timeout=500):
        movetodisableddir.start()

    assert os.path.exists(os.path.join(OptionsManager.getDispath(), 'make game easy mod'))
    assert not os.path.exists(os.path.join(OptionsManager.getGamepath(), 'mods', 'make game easy mod'))

def test_movetodisableddir_cancel(qtbot: QtBot, movetodisableddir: MoveToDisabledDir) -> None:
    movetodisableddir.cancel = True
    with qtbot.wait_signal(movetodisableddir.doneCanceling, timeout=500):
        movetodisableddir.cancelCheck()

    assert not os.path.exists(os.path.join(OptionsManager.getDispath(), 'make game easy mod'))
    assert os.path.exists(os.path.join(OptionsManager.getGamepath(), 'mods', 'make game easy mod'))
