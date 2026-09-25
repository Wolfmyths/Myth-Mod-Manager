import os
import pytest
from collections.abc import Generator

from pytestqt.qtbot import QtBot

from src.objects.change_mod_type import ChangeModType
from src.constant_vars import ModType
from src.helpers.options_manager import OptionsManager

@pytest.fixture(scope="module")
def changemodtype(create_mod_dirs: str, createTemp_Config_ini: str, createTemp_Mod_ini: str) -> Generator[ChangeModType]:  # pyright: ignore[reportUnusedParameter]
    url: str = os.path.join(create_mod_dirs, 'mods', 'make game easy mod')
    url2: str = os.path.join(create_mod_dirs, 'assets', 'mod_overrides', 'best mod ever')

    worker = ChangeModType((url, ModType.mods_override), (url2, ModType.mods))

    yield worker

    worker.deleteLater()

def test_changemodtype(qtbot: QtBot, changemodtype: ChangeModType) -> None:
    with qtbot.wait_signal(changemodtype.succeeded, timeout=500):
        changemodtype.start()

    assert os.path.isdir(os.path.join(OptionsManager.getGamepath(), 'mods', 'make game easy mod')) is False
    assert os.path.isdir(os.path.join(OptionsManager.getGamepath(), 'assets', 'mod_overrides', 'make game easy mod')) is True

def test_changemodtype_cancel(qtbot: QtBot, changemodtype: ChangeModType) -> None:
    changemodtype.cancel = True

    with qtbot.wait_signal(changemodtype.doneCanceling, timeout=500):
        changemodtype.cancelCheck()
    
    assert os.path.isdir(os.path.join(OptionsManager.getGamepath(), 'mods', 'make game easy mod')) is True
    assert os.path.isdir(os.path.join(OptionsManager.getGamepath(), 'assets', 'mod_overrides', 'make game easy mod')) is False
