import pytest
from pytestqt.qtbot import QtBot

from src.settings import Options
from src.constant_vars import DARK

@pytest.fixture(scope='module')
def create_Settings(createTemp_Config_ini: str) -> Options:
    return Options(createTemp_Config_ini)

def test_Settings(qtbot: QtBot, create_Settings: Options) -> None:
    qtbot.addWidget(create_Settings)

@pytest.mark.skip
def test_setGamePath(create_Settings: Options) -> None:
    pass

def test_setDisPath(create_Settings: Options) -> None:
    create_Settings.setDisPath('test')

    assert create_Settings.optionsManager.getDispath() == 'test'

def test_changeColorTheme(create_Settings: Options) -> None:
    create_Settings.changeColorTheme(DARK)

    assert create_Settings.optionsManager.getTheme() == DARK

def test_updateModIgnoreLabel(create_Settings: Options) -> None:
    assert create_Settings.ignoredModsLabel.text() == ''
